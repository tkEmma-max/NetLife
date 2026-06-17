# reports/urls.py
# ============================================
# EXPLANATION: This file defines ALL API endpoints for reports
# Each URL maps to a specific view
# Purpose: To route requests to the correct handler
# ============================================

from django.urls import path
from . import views

# ============================================
# URL PATTERNS
# Each pattern: URL → View → Action
# ============================================

urlpatterns = [
    # ==========================================
    # REPORT MANAGEMENT (Citizens)
    # ==========================================

    # Submit a new report
    # Flutter: POST /api/reports/submit/
    # Action: Creates a new report with evidence
    path('submit/', views.ReportCreateView.as_view(), name='report-create'),

    # List user's reports
    # Flutter: GET /api/reports/my-reports/
    # Action: Returns all reports by current user
    path('my-reports/', views.ReportListView.as_view(), name='report-list'),

    # Get a single report
    # Flutter: GET /api/reports/{id}/
    # Action: Returns details of one report
    path('<int:report_id>/', views.ReportDetailView.as_view(), name='report-detail'),

    # Delete a report (soft delete)
    # Flutter: DELETE /api/reports/{id}/delete/
    # Action: Marks report as inactive
    path('<int:report_id>/delete/', views.DeleteReportView.as_view(), name='report-delete'),

    # ==========================================
    # EVIDENCE MANAGEMENT
    # ==========================================

    # Add more evidence to a report
    # Flutter: POST /api/reports/{id}/add-evidence/
    # Action: Uploads additional evidence files
    path('<int:report_id>/add-evidence/', views.AddEvidenceView.as_view(), name='add-evidence'),

    # ==========================================
    # STATUS MANAGEMENT (Authorities)
    # ==========================================

    # Update report status
    # Flutter: PATCH /api/reports/{id}/status/
    # Action: Verify, reject, or flag report
    path('<int:report_id>/status/', views.ReportStatusUpdateView.as_view(), name='report-status-update'),

    # ==========================================
    # CROWD VERIFICATION
    # ==========================================

    # Verify a report (crowd verification)
    # Flutter: POST /api/reports/{id}/verify/
    # Action: Confirm or deny a report
    path('<int:report_id>/verify/', views.CrowdVerificationView.as_view(), name='crowd-verification'),

    # Get verification responses
    # Flutter: GET /api/reports/{id}/verify/
    # Action: View all verification responses
    path('<int:report_id>/verify/', views.CrowdVerificationView.as_view(), name='crowd-verification-list'),

    # ==========================================
    # LOCATION-BASED QUERIES
    # ==========================================

    # Find nearby reports
    # Flutter: GET /api/reports/nearby/?latitude=4.0514&longitude=9.7019&radius=5
    # Action: Returns reports within radius
    path('nearby/', views.ReportNearbyView.as_view(), name='report-nearby'),

    # ==========================================
    # STATISTICS (Authorities only)
    # ==========================================

    # Get report statistics
    # Flutter: GET /api/reports/stats/
    # Action: Returns statistics about reports
    path('stats/', views.ReportStatsView.as_view(), name='report-stats'),
]