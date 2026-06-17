# ai_engine/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('analyze/<int:report_id>/', views.AnalyzeReportView.as_view(), name='ai-analyze'),
    path('analysis/<int:report_id>/', views.GetAnalysisView.as_view(), name='ai-analysis'),
]