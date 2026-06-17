from django.contrib import admin

# Register your models here.
# interventions/admin.py
# ============================================
# ADMIN POUR L'APPLICATION INTERVENTIONS
# ============================================

from django.contrib import admin
from django.utils.html import format_html
from .models import Intervention, InterventionUpdate


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    """Administration des interventions."""

    list_display = (
        'id',
        'title_preview',
        'team_name',
        'status_badge',
        'alert_link',
        'created_at_short',
        'duration'
    )

    list_filter = ('status', 'team', 'created_at')
    search_fields = ('title', 'description', 'address', 'team__username')
    readonly_fields = ('created_at', 'updated_at', 'resolved_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'description', 'alert', 'team', 'status')
        }),
        ('Localisation', {
            'fields': ('latitude', 'longitude', 'address')
        }),
        ('Suivi', {
            'fields': ('estimated_arrival_minutes', 'actual_arrival_time', 'start_time', 'end_time')
        }),
        ('Notes et résultat', {
            'fields': ('team_notes', 'outcome')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        })
    )

    def title_preview(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title

    title_preview.short_description = 'Titre'

    def team_name(self, obj):
        return obj.team.username if obj.team else 'Non assignée'

    team_name.short_description = 'Équipe'

    def alert_link(self, obj):
        return format_html(f'<a href="/admin/alerts/alert/{obj.alert.id}/">Alert #{obj.alert.id}</a>')

    alert_link.short_description = 'Alerte'

    def status_badge(self, obj):
        colors = {
            'ASSIGNED': '#FFA500',
            'EN_ROUTE': '#FFD700',
            'ON_SITE': '#00C851',
            'IN_PROGRESS': '#2196F3',
            'COMPLETED': '#2C3E50',
            'CANCELLED': '#FF0000'
        }
        color = colors.get(obj.status, '#808080')
        return format_html(
            f'<span style="color:{color};font-weight:bold;">{obj.get_status_display()}</span>'
        )

    status_badge.short_description = 'Statut'
    status_badge.allow_tags = True

    def created_at_short(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    created_at_short.short_description = 'Créé le'

    def duration(self, obj):
        if obj.duration_minutes:
            if obj.duration_minutes < 60:
                return f"{int(obj.duration_minutes)} min"
            else:
                hours = int(obj.duration_minutes / 60)
                minutes = int(obj.duration_minutes % 60)
                return f"{hours}h {minutes}min"
        return '-'

    duration.short_description = 'Durée'


@admin.register(InterventionUpdate)
class InterventionUpdateAdmin(admin.ModelAdmin):
    """Administration des mises à jour d'interventions."""

    list_display = ('id', 'intervention_link', 'updated_by', 'old_status', 'new_status', 'created_at')
    list_filter = ('old_status', 'new_status', 'created_at')
    search_fields = ('intervention__title', 'updated_by__username', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def intervention_link(self, obj):
        return f"Intervention #{obj.intervention.id}"

    intervention_link.short_description = 'Intervention'