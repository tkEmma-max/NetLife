from django.contrib import admin

# Register your models here.
# reports/admin.py
# ============================================
# EXPLANATION: Django Admin Panel Configuration
# This makes it easy to manage reports from the admin interface
# Purpose: To view, filter, and manage reports without using the API
# ============================================

from django.contrib import admin
from django.utils.html import format_html
from .models import Report, ReportEvidence, CrowdVerification


# ============================================
# INLINE ADMIN: Evidence
# Shows evidence files inside the report admin page
# ============================================

class ReportEvidenceInline(admin.TabularInline):
    """
    Display evidence files as inline in the report admin page.

    Purpose: To see all evidence files for a report in one place
    """
    model = ReportEvidence
    extra = 1  # Allow adding 1 new evidence
    fields = ('file', 'evidence_type', 'original_filename', 'file_size', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

    def get_queryset(self, request):
        """Order evidence by upload date (newest first)"""
        return super().get_queryset(request).order_by('-uploaded_at')


# ============================================
# INLINE ADMIN: Crowd Verification
# Shows crowd verification responses
# ============================================

class CrowdVerificationInline(admin.TabularInline):
    """
    Display crowd verification responses as inline.

    Purpose: To see all crowd responses for a report
    """
    model = CrowdVerification
    extra = 0
    fields = ('citizen', 'response', 'comment', 'responded_at')
    readonly_fields = ('responded_at',)


# ============================================
# MAIN ADMIN: Report
# ============================================

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Admin interface for Report model.

    Purpose: To manage reports from Django admin panel
    """

    # ============================================
    # LIST VIEW - What columns to show
    # ============================================

    list_display = (
        'id',
        'title_preview',
        'reporter_email',
        'danger_type_tag',
        'severity_badge',
        'status_badge',
        'is_verified',
        'created_at_short',
        'evidence_count'
    )

    # ============================================
    # FILTERS - Filter reports by these fields
    # ============================================

    list_filter = (
        'status',
        'danger_type',
        'is_verified',
        'is_active',
        'created_at',
        'reporter__role'
    )

    # ============================================
    # SEARCH - Search by these fields
    # ============================================

    search_fields = (
        'title',
        'description',
        'address',
        'reporter__email',
        'reporter__username',
        'id'
    )

    # ============================================
    # READONLY FIELDS - Cannot be edited
    # ============================================

    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
        'verified_at',
        'resolved_at',
        'points_awarded',
        'money_earned_cfa'
    )

    # ============================================
    # ORDERING - Default sort order
    # ============================================

    ordering = ('-created_at',)

    # ============================================
    # INLINES - Show related data
    # ============================================

    inlines = [ReportEvidenceInline, CrowdVerificationInline]

    # ============================================
    # FIELDSETS - Organize the edit form
    # ============================================

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'description',
                'reporter'
            )
        }),
        ('Classification', {
            'fields': (
                'danger_type',
                'severity',
                'confidence_score'
            )
        }),
        ('Location', {
            'fields': (
                'latitude',
                'longitude',
                'address',
                'gps_accuracy'
            )
        }),
        ('Status', {
            'fields': (
                'status',
                'is_verified',
                'verified_by',
                'is_active'
            )
        }),
        ('Crowd Verification', {
            'fields': (
                'crowd_confirmations',
                'crowd_denials',
                'crowd_verification_completed'
            )
        }),
        ('Rewards', {
            'fields': (
                'points_awarded',
                'money_earned_cfa'
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
                'verified_at',
                'resolved_at'
            ),
            'classes': ('collapse',)  # Collapsible section
        }),
        ('Metadata', {
            'fields': (
                'id',
                'device_model',
                'app_version'
            ),
            'classes': ('collapse',)
        })
    )

    # ============================================
    # CUSTOM METHODS (For display formatting)
    # ============================================

    def title_preview(self, obj):
        """Shorten title for list view"""
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title

    title_preview.short_description = 'Title'

    def reporter_email(self, obj):
        """Show reporter's email"""
        return obj.reporter.email

    reporter_email.short_description = 'Reporter'

    def created_at_short(self, obj):
        """Show created date in short format"""
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    created_at_short.short_description = 'Created'
    created_at_short.admin_order_field = 'created_at'

    def evidence_count(self, obj):
        """Count evidence files"""
        count = obj.evidence.count()
        return f"📎 {count}"

    evidence_count.short_description = 'Evidence'

    def danger_type_tag(self, obj):
        """Display danger type with emoji"""
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
        return format_html(f"{emoji} {obj.get_danger_type_display() if obj.danger_type else 'Unknown'}")

    danger_type_tag.short_description = 'Type'

    def severity_badge(self, obj):
        """Display severity with color coding"""
        if not obj.severity:
            return '-'

        if obj.severity >= 8:
            color = '#FF0000'  # Red - Critical
            emoji = '🔴'
        elif obj.severity >= 5:
            color = '#FFA500'  # Orange - High
            emoji = '🟠'
        elif obj.severity >= 3:
            color = '#FFD700'  # Yellow - Medium
            emoji = '🟡'
        else:
            color = '#00C851'  # Green - Low
            emoji = '🟢'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color, emoji, obj.severity
        )

    severity_badge.short_description = 'Severity'

    def status_badge(self, obj):
        """Display status with color coding"""
        status_colors = {
            'PENDING_AI': '#FFA500',  # Orange
            'CROWD_VERIFY': '#FFD700',  # Yellow
            'VERIFIED': '#00C851',  # Green
            'REJECTED': '#FF0000',  # Red
            'FLAGGED': '#FF6B6B',  # Light Red
            'ALERT_CREATED': '#FF4444',  # Bright Red
            'RESOLVED': '#2C3E50'  # Dark Blue
        }

        status_labels = {
            'PENDING_AI': '⏳ Pending AI',
            'CROWD_VERIFY': '👥 Crowd Verify',
            'VERIFIED': '✅ Verified',
            'REJECTED': '❌ Rejected',
            'FLAGGED': '🚩 Flagged',
            'ALERT_CREATED': '🚨 Alert Created',
            'RESOLVED': '✔️ Resolved'
        }

        color = status_colors.get(obj.status, '#808080')
        label = status_labels.get(obj.status, obj.status)

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, label
        )

    status_badge.short_description = 'Status'

    # ============================================
    # ACTIONS - Batch operations
    # ============================================

    actions = ['mark_as_verified', 'mark_as_resolved', 'mark_as_rejected']

    def mark_as_verified(self, request, queryset):
        """Batch mark reports as verified"""
        updated = queryset.update(
            status='VERIFIED',
            is_verified=True,
            verified_at=timezone.now()
        )
        self.message_user(request, f"{updated} reports marked as verified.")

    mark_as_verified.short_description = "Mark selected as Verified"

    def mark_as_resolved(self, request, queryset):
        """Batch mark reports as resolved"""
        updated = queryset.update(
            status='RESOLVED',
            resolved_at=timezone.now()
        )
        self.message_user(request, f"{updated} reports marked as resolved.")

    mark_as_resolved.short_description = "Mark selected as Resolved"

    def mark_as_rejected(self, request, queryset):
        """Batch mark reports as rejected"""
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f"{updated} reports marked as rejected.")

    mark_as_rejected.short_description = "Mark selected as Rejected"


# ============================================
# EVIDENCE ADMIN
# ============================================

@admin.register(ReportEvidence)
class ReportEvidenceAdmin(admin.ModelAdmin):
    """
    Admin interface for ReportEvidence model.
    """
    list_display = ('id', 'report_preview', 'evidence_type', 'original_filename', 'file_size', 'uploaded_at')
    list_filter = ('evidence_type', 'uploaded_at')
    search_fields = ('original_filename', 'report__title', 'report__reporter__email')
    readonly_fields = ('uploaded_at',)
    ordering = ('-uploaded_at',)

    def report_preview(self, obj):
        """Show report title"""
        return f"Report #{obj.report.id} - {obj.report.title[:30]}"

    report_preview.short_description = 'Report'


# ============================================
# CROWD VERIFICATION ADMIN
# ============================================

@admin.register(CrowdVerification)
class CrowdVerificationAdmin(admin.ModelAdmin):
    """
    Admin interface for CrowdVerification model.
    """
    list_display = ('id', 'report_preview', 'citizen_email', 'response_badge', 'responded_at')
    list_filter = ('response', 'responded_at')
    search_fields = ('report__title', 'citizen__email')
    readonly_fields = ('responded_at',)
    ordering = ('-responded_at',)

    def report_preview(self, obj):
        """Show report title"""
        return f"Report #{obj.report.id}"

    report_preview.short_description = 'Report'

    def citizen_email(self, obj):
        """Show citizen email"""
        return obj.citizen.email

    citizen_email.short_description = 'Citizen'

    def response_badge(self, obj):
        """Display response with color"""
        response_colors = {
            'CONFIRM': '#00C851',  # Green
            'DENY': '#FF0000',  # Red
            'UNSURE': '#FFA500'  # Orange
        }
        color = response_colors.get(obj.response, '#808080')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_response_display()
        )

    response_badge.short_description = 'Response'