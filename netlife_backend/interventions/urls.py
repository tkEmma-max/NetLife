# interventions/urls.py
# ============================================
# ROUTAGE POUR L'APPLICATION INTERVENTIONS
# ============================================

from django.urls import path
from . import views

urlpatterns = [
    # Créer une intervention
    path('create/', views.CreateInterventionView.as_view(), name='create-intervention'),

    # Interventions actives
    path('active/', views.ActiveInterventionsView.as_view(), name='active-interventions'),

    # Détails d'une intervention
    path('<int:intervention_id>/', views.InterventionDetailView.as_view(), name='intervention-detail'),

    # Mettre à jour le statut
    path('<int:intervention_id>/status/', views.UpdateInterventionStatusView.as_view(), name='update-status'),

    # Mises à jour d'une intervention
    path('<int:intervention_id>/updates/', views.InterventionUpdatesView.as_view(), name='intervention-updates'),

    # Ajouter une note
    path('<int:intervention_id>/add-note/', views.AddNoteView.as_view(), name='add-note'),

    # Interventions d'une équipe
    path('team/<int:team_id>/', views.TeamInterventionsView.as_view(), name='team-interventions'),
]