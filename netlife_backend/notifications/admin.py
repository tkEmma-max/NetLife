from django.contrib import admin

# Register your models here.
# notifications/admin.py
# ============================================
# ADMIN POUR L'APPLICATION NOTIFICATIONS
# ============================================

from django.contrib import admin
from django.utils.html import format_html
from .models import Notification, FCMDevice


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Administration des notifications."""

    list_display = (
        'id',
        'title_preview',
        'recipient_email',
        'notification_type_badge',
        'channel_badge',
        'is_read_badge',
        'is_sent_badge',
        'created_at_short'
    )

    list_filter = ('notification_type', 'channel', 'is_read', 'is_sent', 'created_at')
    search_fields = ('title', 'message', 'recipient__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Informations principales', {
            'fields': ('recipient', 'notification_type', 'title', 'message', 'channel')
        }),
        ('Données associées', {
            'fields': ('alert', 'intervention', 'data', 'image_url')
        }),
        ('Statut', {
            'fields': ('is_read', 'read_at', 'is_sent', 'sent_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def title_preview(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title

    title_preview.short_description = 'Titre'

    def recipient_email(self, obj):
        return obj.recipient.email

    recipient_email.short_description = 'Destinataire'

    def notification_type_badge(self, obj):
        colors = {
            'ALERT': '#FF0000',
            'INTERVENTION': '#FFA500',
            'REPORT_VERIFIED': '#00C851',
            'POINTS_AWARDED': '#FFD700',
            'POINTS_REDEEMED': '#FF6B00',
            'STATUS_UPDATE': '#2196F3',
            'RESOLVED': '#2C3E50',
            'SYSTEM': '#808080'
        }
        color = colors.get(obj.notification_type, '#808080')
        return format_html(
            f'<span style="color:{color};font-weight:bold;">{obj.get_notification_type_display()}</span>'
        )

    notification_type_badge.short_description = 'Type'
    notification_type_badge.allow_tags = True

    def channel_badge(self, obj):
        icons = {
            'PUSH': '📲',
            'EMAIL': '📧',
            'SMS': '📱',
            'IN_APP': '🔔'
        }
        icon = icons.get(obj.channel, '📨')
        return format_html(f'{icon} {obj.get_channel_display()}')

    channel_badge.short_description = 'Canal'
    channel_badge.allow_tags = True

    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html('✅ Lu')
        return format_html('🔴 Non lu')

    is_read_badge.short_description = 'Lu'
    is_read_badge.allow_tags = True

    def is_sent_badge(self, obj):
        if obj.is_sent:
            return format_html('✅ Envoyé')
        return format_html('⏳ En attente')

    is_sent_badge.short_description = 'Envoyé'
    is_sent_badge.allow_tags = True

    def created_at_short(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    created_at_short.short_description = 'Créé le'


@admin.register(FCMDevice)
class FCMDeviceAdmin(admin.ModelAdmin):
    """Administration des appareils FCM."""

    list_display = ('id', 'user_email', 'device_type', 'fcm_token_short', 'is_active', 'created_at')
    list_filter = ('device_type', 'is_active', 'created_at')
    search_fields = ('user__email', 'fcm_token')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Utilisateur'

    def fcm_token_short(self, obj):
        return f"{obj.fcm_token[:30]}..."

    fcm_token_short.short_description = 'Token FCM'