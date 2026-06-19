from django.shortcuts import render

# Create your views here.
# alerts/views.py
# ============================================
# EXPLANATION: API Views for Alerts
# ============================================

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from reports.models import Report
from .models import Alert, AlertLog
from .serializers import AlertSerializer, AlertLogSerializer
from .services import AlertService


class ActiveAlertsView(APIView):
    """Get all active alerts."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        alerts = Alert.objects.filter(
            is_active=True,
            status__in=[Alert.Status.ACTIVE, Alert.Status.IN_PROGRESS]
        ).order_by('-created_at')

        serializer = AlertSerializer(alerts, many=True, context={'request': request})
        return Response(serializer.data)


class AlertDetailView(APIView):
    """Get alert details."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, alert_id):
        alert = get_object_or_404(Alert, id=alert_id)
        serializer = AlertSerializer(alert, context={'request': request})
        return Response(serializer.data)


class CreateAlertView(APIView):
    """Create alert from a verified report."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, report_id):
        # Check if user is authority
        if not (request.user.is_authority or request.user.is_admin):
            return Response(
                {'error': 'Only authorities can create alerts.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get report
        report = get_object_or_404(Report, id=report_id)

        # Check if report is verified
        if not report.is_verified:
            return Response(
                {'error': 'Report must be verified before creating an alert.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if alert already exists
        if hasattr(report, 'alert'):
            return Response(
                {'error': 'Alert already exists for this report.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create alert
        alert_service = AlertService()
        alert = alert_service.create_alert(report, request.user)

        serializer = AlertSerializer(alert, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateAlertStatusView(APIView):
    """Update alert status."""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, alert_id):
        # Check if user is authority or team
        if not (request.user.is_authority or request.user.is_admin or request.user.is_intervention_team):
            return Response(
                {'error': 'Only authorities and teams can update alert status.'},
                status=status.HTTP_403_FORBIDDEN
            )

        alert = get_object_or_404(Alert, id=alert_id)

        status_val = request.data.get('status')
        if status_val not in [Alert.Status.ACTIVE, Alert.Status.IN_PROGRESS,
                              Alert.Status.RESOLVED, Alert.Status.CLOSED]:
            return Response(
                {'error': 'Invalid status value.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update status
        alert_service = AlertService()
        alert = alert_service.update_status(alert, status_val, request.user)

        serializer = AlertSerializer(alert, context={'request': request})
        return Response(serializer.data)


class AssignTeamView(APIView):
    """Assign an intervention team to an alert."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, alert_id):
        if not (request.user.is_authority or request.user.is_admin):
            return Response(
                {'error': 'Only authorities can assign teams.'},
                status=status.HTTP_403_FORBIDDEN
            )

        alert = get_object_or_404(Alert, id=alert_id)
        team_id = request.data.get('team_id')

        if not team_id:
            return Response(
                {'error': 'team_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        alert_service = AlertService()
        alert = alert_service.assign_team(alert, team_id, request.user)

        serializer = AlertSerializer(alert, context={'request': request})
        return Response(serializer.data)


class AlertHistoryView(APIView):
    """Get alert history/logs."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, alert_id):
        alert = get_object_or_404(Alert, id=alert_id)
        logs = alert.logs.all().order_by('-timestamp')
        serializer = AlertLogSerializer(logs, many=True)
        return Response(serializer.data)


class NearbyAlertsView(APIView):
    """Get alerts near a user's location."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        radius = request.query_params.get('radius', 5)  # Default 5km

        if not latitude or not longitude:
            return Response(
                {'error': 'latitude and longitude are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get active alerts
        alerts = Alert.objects.filter(
            is_active=True,
            status__in=[Alert.Status.ACTIVE, Alert.Status.IN_PROGRESS]
        )

        # Filter by distance
        try:
            lat = float(latitude)
            lng = float(longitude)
            radius_km = float(radius)

            # Approximate 1 degree = 111km
            delta = radius_km / 111

            alerts = alerts.filter(
                latitude__gte=lat - delta,
                latitude__lte=lat + delta,
                longitude__gte=lng - delta,
                longitude__lte=lng + delta
            )
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid latitude/longitude/radius.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AlertSerializer(alerts, many=True, context={'request': request})
        return Response(serializer.data)