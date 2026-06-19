# alerts/urls.py
# ============================================
# EXPLANATION: URL Routing for Alerts
# ============================================

from django.urls import path
from . import views

urlpatterns = [
    # Get active alerts
    path('active/', views.ActiveAlertsView.as_view(), name='active-alerts'),

    # Get alert details
    path('<int:alert_id>/', views.AlertDetailView.as_view(), name='alert-detail'),

    # Create alert from report
    path('create/<int:report_id>/', views.CreateAlertView.as_view(), name='create-alert'),

    # Update alert status
    path('<int:alert_id>/status/', views.UpdateAlertStatusView.as_view(), name='update-status'),

    # Assign team to alert
    path('<int:alert_id>/assign-team/', views.AssignTeamView.as_view(), name='assign-team'),

    # Get alert history
    path('<int:alert_id>/history/', views.AlertHistoryView.as_view(), name='alert-history'),

    # Get nearby alerts
    path('nearby/', views.NearbyAlertsView.as_view(), name='nearby-alerts'),
]