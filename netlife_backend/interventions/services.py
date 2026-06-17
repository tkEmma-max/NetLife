# interventions/services.py
# ============================================
# SERVICES POUR L'APPLICATION INTERVENTIONS
# ============================================

from django.utils import timezone
from django.shortcuts import get_object_or_404
from alerts.models import Alert
from accounts.models import User
from .models import Intervention, InterventionUpdate


class InterventionService:
    """Service pour la gestion des interventions."""

    def create_intervention(self, alert_id, team_id, created_by, notes=""):
        """Créer une intervention à partir d'une alerte."""

        # Récupérer l'alerte
        alert = get_object_or_404(Alert, id=alert_id)

        # Vérifier si l'alerte a déjà une intervention
        if hasattr(alert, 'intervention'):
            raise ValueError("Cette alerte a déjà une intervention.")

        # Récupérer l'équipe
        team = get_object_or_404(User, id=team_id, role='INTERVENTION_TEAM')

        # Créer l'intervention
        intervention = Intervention.objects.create(
            alert=alert,
            team=team,
            created_by=created_by,
            title=f"🚒 Intervention - {alert.title}",
            description=alert.description,
            latitude=alert.latitude,
            longitude=alert.longitude,
            address=alert.address,
            status=Intervention.Status.ASSIGNED,
            team_notes=notes
        )

        # Mettre à jour l'alerte
        alert.mark_as_in_progress(team)

        # Créer un log de création
        InterventionUpdate.objects.create(
            intervention=intervention,
            updated_by=created_by,
            old_status=intervention.status,
            new_status=intervention.status,
            message=f"Intervention créée. Équipe {team.username} assignée."
        )

        return intervention

    def update_status(self, intervention, new_status, updated_by, message=""):
        """Mettre à jour le statut d'une intervention."""

        old_status = intervention.status

        # Mettre à jour le statut
        intervention.status = new_status

        # Actions spécifiques selon le statut
        if new_status == Intervention.Status.EN_ROUTE:
            # L'équipe est en route
            pass

        elif new_status == Intervention.Status.ON_SITE:
            intervention.actual_arrival_time = timezone.now()

        elif new_status == Intervention.Status.IN_PROGRESS:
            if not intervention.start_time:
                intervention.start_time = timezone.now()

        elif new_status == Intervention.Status.COMPLETED:
            intervention.end_time = timezone.now()
            intervention.resolved_at = timezone.now()
            if not intervention.outcome:
                intervention.outcome = "Intervention terminée avec succès."
            # Mettre à jour l'alerte
            if hasattr(intervention, 'alert'):
                intervention.alert.mark_as_resolved(updated_by)

        elif new_status == Intervention.Status.CANCELLED:
            intervention.resolved_at = timezone.now()
            if not message:
                message = "Intervention annulée."

        intervention.save()

        # Ajouter la note
        if message:
            intervention.add_note(message)

        # Créer un log de mise à jour
        InterventionUpdate.objects.create(
            intervention=intervention,
            updated_by=updated_by,
            old_status=old_status,
            new_status=new_status,
            message=message or f"Statut changé de {old_status} à {new_status}"
        )

        return intervention

    def get_intervention_updates(self, intervention):
        """Récupérer toutes les mises à jour d'une intervention."""
        return intervention.updates.all().order_by('-created_at')

    def get_active_interventions(self):
        """Récupérer toutes les interventions actives."""
        return Intervention.objects.filter(
            status__in=[
                Intervention.Status.ASSIGNED,
                Intervention.Status.EN_ROUTE,
                Intervention.Status.ON_SITE,
                Intervention.Status.IN_PROGRESS
            ]
        ).order_by('-created_at')

    def get_team_interventions(self, team_id):
        """Récupérer toutes les interventions d'une équipe."""
        return Intervention.objects.filter(
            team_id=team_id
        ).order_by('-created_at')