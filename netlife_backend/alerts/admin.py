from django.contrib import admin

# Register your models here.
# alerts/admin.py
# ============================================
# EXPLANATION: Admin Configuration for Alerts
# ============================================

from django.contrib import admin
from django.utils.html import format_html
from .models import Alert, AlertLog


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title_preview',
        'danger_type_tag',
        'priority_badge',
        'status_badge',
        'created_at_short'
    )
    list_filter = ('status', 'priority', 'danger_type', 'created_at')
    search_fields = ('title', 'description', 'address')
    readonly_fields = ('created_at', 'updated_at', 'resolved_at', 'closed_at')
    ordering = ('-created_at',)

    def title_preview(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title

    title_preview.short_description = 'Title'

    def danger_type_tag(self, obj):
        emojis = {
            'FIRE': '🔥',
            'FLOOD': '🌊',
            'WASTE': '🗑️',
            'DEFORESTATION': '🌳',
            'POLLUTION': '☠️',
            'ROAD_HAZARD': '🚧',
            'OTHER': '⚠️'
        }
        emoji = emojis.get(obj.danger_type, '❓')
        return format_html(f"{emoji} {obj.get_danger_type_display()}")

    danger_type_tag.short_description = 'Type'

    def priority_badge(self, obj):
        colors = {
            'LOW': '#00C851',
            'MEDIUM': '#FFD700',
            'HIGH': '#FFA500',
            'CRITICAL': '#FF0000'
        }
        color = colors.get(obj.priority, '#808080')
        return format_html(f'<span style="color:{color};font-weight:bold;">{obj.get_priority_display()}</span>')

    priority_badge.short_description = 'Priority'
    priority_badge.allow_tags = True

    def status_badge(self, obj):
        colors = {
            'ACTIVE': '#FF0000',
            'IN_PROGRESS': '#FFA500',
            'RESOLVED': '#00C851',
            'CLOSED': '#808080'
        }
        color = colors.get(obj.status, '#808080')
        return format_html(f'<span style="color:{color};font-weight:bold;">{obj.get_status_display()}</span>')

    status_badge.short_description = 'Status'
    status_badge.allow_tags = True

    def created_at_short(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    created_at_short.short_description = 'Created'


@admin.register(AlertLog)
class AlertLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'alert', 'action_type', 'performed_by', 'timestamp')
    list_filter = ('action_type', 'timestamp')
    search_fields = ('alert__title', 'performed_by__email')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)