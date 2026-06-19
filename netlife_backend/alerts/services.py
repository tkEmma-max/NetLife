# alerts/services.py
# ============================================
# EXPLANATION: Alert Business Logic
# ============================================

from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Alert, AlertLog
from reports.models import Report
from accounts.models import User


class AlertService:
    """Service for managing alerts."""

    def create_alert(self, report, created_by):
        """Create an alert from a verified report."""

        # Determine priority from severity
        priority = self._determine_priority(report.severity)

        # Create the alert
        alert = Alert.objects.create(
            report=report,
            title=f"🚨 {report.get_danger_type_display()} - {report.title}",
            description=report.description,
            danger_type=report.danger_type,
            priority=priority,
            severity=report.severity,
            latitude=report.latitude,
            longitude=report.longitude,
            address=report.address,
            created_by=created_by,
            status=Alert.Status.ACTIVE,
            alert_radius_km=1.0  # Default 1km radius
        )

        # Log the creation
        self._log_action(alert, 'CREATED', created_by, {
            'report_id': report.id,
            'severity': report.severity,
            'priority': priority
        })

        # Send notifications to nearby citizens
        self._broadcast_alert(alert)

        return alert

    def update_status(self, alert, new_status, user):
        """Update alert status."""
        old_status = alert.status
        alert.status = new_status

        if new_status == Alert.Status.RESOLVED:
            alert.resolved_at = timezone.now()
            alert.is_active = False
            if hasattr(alert, 'report') and alert.report:
                alert.report.mark_as_resolved()

        if new_status == Alert.Status.CLOSED:
            alert.closed_at = timezone.now()
            alert.is_active = False

        alert.save()

        # Log the status change
        self._log_action(alert, 'STATUS_CHANGE', user, {
            'old_status': old_status,
            'new_status': new_status
        })

        return alert

    def assign_team(self, alert, team_id, assigned_by):
        """Assign an intervention team to an alert."""
        team = get_object_or_404(User, id=team_id, role='INTERVENTION_TEAM')

        alert.assigned_team = team
        alert.status = Alert.Status.IN_PROGRESS
        alert.save()

        # Log the assignment
        self._log_action(alert, 'TEAM_ASSIGNED', assigned_by, {
            'team_id': team.id,
            'team_name': team.username
        })

        # Send notification to team
        self._notify_team(alert, team)

        return alert

    def _determine_priority(self, severity):
        """Determine priority from severity score."""
        if severity >= 8:
            return Alert.Priority.CRITICAL
        elif severity >= 6:
            return Alert.Priority.HIGH
        elif severity >= 4:
            return Alert.Priority.MEDIUM
        else:
            return Alert.Priority.LOW

    def _log_action(self, alert, action_type, user, details):
        """Log an action."""
        AlertLog.objects.create(
            alert=alert,
            action_type=action_type,
            performed_by=user,
            details=details
        )

    def _broadcast_alert(self, alert):
        """Broadcast alert to nearby citizens."""
        # Get citizens within radius
        # Approximate 1 degree = 111km
        delta = alert.alert_radius_km / 111

        nearby_citizens = User.objects.filter(
            role='CITIZEN',
            is_active=True,
            latitude__gte=float(alert.latitude) - delta,
            latitude__lte=float(alert.latitude) + delta,
            longitude__gte=float(alert.longitude) - delta,
            longitude__lte=float(alert.longitude) + delta
        )

        # Update notification count
        alert.citizens_notified = nearby_citizens.count()
        alert.save()

        # Log notification
        self._log_action(alert, 'NOTIFICATION_SENT', alert.created_by, {
            'citizens_notified': alert.citizens_notified,
            'radius_km': alert.alert_radius_km
        })

        # TODO: Send actual push notifications via Firebase
        print(f"📢 Alert #{alert.id} broadcasted to {alert.citizens_notified} citizens")

        return nearby_citizens

    def _notify_team(self, alert, team):
        """Send notification to assigned team."""
        # TODO: Implement push notification to team
        print(f"📢 Team {team.username} assigned to Alert #{alert.id}")
