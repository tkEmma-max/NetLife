# notifications/serializers.py
# ============================================
# SERIALIZERS POUR L'APPLICATION NOTIFICATIONS
# ============================================

from rest_framework import serializers
from .models import Notification, FCMDevice


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Notification."""

    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )
    channel_display = serializers.CharField(
        source='get_channel_display',
        read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'alert',
            'intervention',
            'notification_type',
            'notification_type_display',
            'title',
            'message',
            'channel',
            'channel_display',
            'data',
            'image_url',
            'is_read',
            'is_sent',
            'read_at',
            'sent_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'recipient',
            'created_at',
            'updated_at',
        ]


class FCMDeviceSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle FCMDevice."""

    class Meta:
        model = FCMDevice
        fields = [
            'id',
            'user',
            'fcm_token',
            'device_type',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class NotificationCreateSerializer(serializers.Serializer):
    """Serializer pour la création d'une notification."""

    recipient_id = serializers.IntegerField(required=True)
    notification_type = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    channel = serializers.CharField(default='IN_APP')
    data = serializers.JSONField(default=dict)
    image_url = serializers.URLField(required=False, allow_blank=True)
    alert_id = serializers.IntegerField(required=False, allow_null=True)
    intervention_id = serializers.IntegerField(required=False, allow_null=True)