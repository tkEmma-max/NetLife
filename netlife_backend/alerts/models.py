from django.db import models

# Create your models here.
# alerts/models.py
# ============================================
# EXPLANATION: Database models for Alerts
# ============================================

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Alert(models.Model):
    """
    Emergency Alert model.

    Purpose: To track emergency alerts created from verified reports
    Who uses it: Authorities create, Citizens receive, Teams respond
    """

    # ============================================
    # STATUS CHOICES
    # ============================================

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'
        CLOSED = 'CLOSED', 'Closed'

    # ============================================
    # PRIORITY CHOICES
    # ============================================

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    # ============================================
    # RELATIONSHIPS
    # ============================================

    # The report that triggered this alert
    report = models.OneToOneField(
        'reports.Report',
        on_delete=models.CASCADE,
        related_name='alert',
        help_text="The report that triggered this alert"
    )

    # Who created this alert?
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_alerts',
        help_text="Authority who created this alert"
    )

    # Who resolved this alert?
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_alerts',
        help_text="Authority who resolved this alert"
    )

    # Assigned intervention team
    assigned_team = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_alerts',
        limit_choices_to={'role': 'INTERVENTION_TEAM'},
        help_text="Intervention team assigned to this alert"
    )

    # ============================================
    # ALERT DETAILS
    # ============================================

    # Title
    title = models.CharField(
        max_length=200,
        help_text="Alert title"
    )

    # Description
    description = models.TextField(
        help_text="Detailed alert description"
    )

    # Danger type (from Report)
    danger_type = models.CharField(
        max_length=20,
        help_text="Type of danger"
    )

    # Priority level
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        help_text="Alert priority level"
    )

    # Severity score (1-10)
    severity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Severity score (1-10)"
    )

    # ============================================
    # LOCATION
    # ============================================

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        help_text="Alert latitude"
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        help_text="Alert longitude"
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Human-readable address"
    )

    # Alert radius (in km) - who gets notified
    alert_radius_km = models.FloatField(
        default=1.0,
        help_text="Radius in kilometers for alert broadcasting"
    )

    # ============================================
    # STATUS
    # ============================================

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        help_text="Current alert status"
    )

    # ============================================
    # TIMESTAMPS
    # ============================================

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    # ============================================
    # METADATA
    # ============================================

    # Number of citizens notified
    citizens_notified = models.IntegerField(
        default=0,
        help_text="Number of citizens who received this alert"
    )

    # Number of citizens who confirmed receiving
    citizens_confirmed = models.IntegerField(
        default=0,
        help_text="Number of citizens who confirmed receiving"
    )

    # Is this alert still active?
    is_active = models.BooleanField(
        default=True,
        help_text="Is this alert still active?"
    )

    # ============================================
    # META CLASS
    # ============================================

    class Meta:
        db_table = 'alerts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['danger_type']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_active']),
        ]

    # ============================================
    # STRING REPRESENTATION
    # ============================================

    def __str__(self):
        return f"Alert #{self.id}: {self.title} ({self.get_status_display()})"

    # ============================================
    # PROPERTIES
    # ============================================

    @property
    def is_critical(self):
        """Check if this is a critical alert."""
        return self.priority == self.Priority.CRITICAL

    @property
    def is_high_priority(self):
        """Check if this is high priority or above."""
        return self.priority in [self.Priority.HIGH, self.Priority.CRITICAL]

    @property
    def duration_minutes(self):
        """Calculate how long this alert has been active."""
        if self.resolved_at:
            return (self.resolved_at - self.created_at).total_seconds() / 60
        return (timezone.now() - self.created_at).total_seconds() / 60

    def get_priority_color(self):
        """Get color for priority display."""
        colors = {
            'LOW': '#00C851',
            'MEDIUM': '#FFD700',
            'HIGH': '#FFA500',
            'CRITICAL': '#FF0000'
        }
        return colors.get(self.priority, '#808080')

    # ============================================
    # METHODS
    # ============================================

    def mark_as_in_progress(self, team):
        """Mark alert as in progress with assigned team."""
        self.status = self.Status.IN_PROGRESS
        self.assigned_team = team
        self.save()
        return self

    def mark_as_resolved(self, resolver):
        """Mark alert as resolved."""
        self.status = self.Status.RESOLVED
        self.resolved_by = resolver
        self.resolved_at = timezone.now()
        self.is_active = False
        self.save()

        # Also update the report
        if hasattr(self, 'report'):
            self.report.mark_as_resolved()

        return self

    def mark_as_closed(self):
        """Close the alert."""
        self.status = self.Status.CLOSED
        self.closed_at = timezone.now()
        self.is_active = False
        self.save()
        return self


# ============================================
# MODEL 2: AlertLog
# Tracks all actions taken on an alert
# ============================================

class AlertLog(models.Model):
    """
    Audit log for alert actions.

    Purpose: To track who did what and when
    """

    class ActionType(models.TextChoices):
        CREATED = 'CREATED', 'Alert Created'
        STATUS_CHANGE = 'STATUS_CHANGE', 'Status Changed'
        TEAM_ASSIGNED = 'TEAM_ASSIGNED', 'Team Assigned'
        NOTIFICATION_SENT = 'NOTIFICATION_SENT', 'Notification Sent'
        RESOLVED = 'RESOLVED', 'Alert Resolved'
        CLOSED = 'CLOSED', 'Alert Closed'

    alert = models.ForeignKey(
        Alert,
        on_delete=models.CASCADE,
        related_name='logs',
        help_text="The alert this log belongs to"
    )

    action_type = models.CharField(
        max_length=20,
        choices=ActionType.choices,
        help_text="Type of action"
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Who performed this action"
    )

    details = models.JSONField(
        default=dict,
        help_text="Additional details about the action"
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alert_logs'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_action_type_display()} - Alert #{self.alert.id}"