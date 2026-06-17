# alerts/serializers.py
# ============================================
# EXPLANATION: Serializers for Alerts
# ============================================

from rest_framework import serializers
from .models import Alert, AlertLog
from reports.serializers import ReportSerializer


class AlertSerializer(serializers.ModelSerializer):
    """Serializer for Alert model."""

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    priority_color = serializers.CharField(read_only=True)
    duration_minutes = serializers.FloatField(read_only=True)
    is_critical = serializers.BooleanField(read_only=True)

    # Nested report data
    report = ReportSerializer(read_only=True)

    # User info
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    assigned_team_name = serializers.CharField(source='assigned_team.username', read_only=True, default=None)

    class Meta:
        model = Alert
        fields = [
            'id',
            'report',
            'title',
            'description',
            'danger_type',
            'priority',
            'priority_display',
            'priority_color',
            'severity',
            'latitude',
            'longitude',
            'address',
            'alert_radius_km',
            'status',
            'status_display',
            'created_by',
            'created_by_email',
            'assigned_team',
            'assigned_team_name',
            'citizens_notified',
            'citizens_confirmed',
            'is_active',
            'is_critical',
            'duration_minutes',
            'created_at',
            'updated_at',
            'resolved_at',
        ]
        read_only_fields = [
            'id',
            'created_by',
            'created_at',
            'updated_at',
            'resolved_at',
            'citizens_notified',
            'citizens_confirmed',
        ]


class AlertLogSerializer(serializers.ModelSerializer):
    """Serializer for AlertLog model."""

    action_display = serializers.CharField(source='get_action_type_display', read_only=True)
    performed_by_email = serializers.EmailField(source='performed_by.email', read_only=True)

    class Meta:
        model = AlertLog
        fields = [
            'id',
            'alert',
            'action_type',
            'action_display',
            'performed_by',
            'performed_by_email',
            'details',
            'timestamp',
        ]
        read_only_fields = ['id', 'timestamp']