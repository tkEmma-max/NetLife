from django.db import models

# Create your models here.
# interventions/models.py
# ============================================
# MODÈLES POUR L'APPLICATION INTERVENTIONS
# ============================================

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Intervention(models.Model):
    """
    Modèle principal pour les interventions.

    Une intervention est créée à partir d'une alerte et suivie par une équipe.
    """

    # ============================================
    # STATUTS DE L'INTERVENTION
    # ============================================

    class Status(models.TextChoices):
        ASSIGNED = 'ASSIGNED', 'Assignée'
        EN_ROUTE = 'EN_ROUTE', 'En route'
        ON_SITE = 'ON_SITE', 'Sur place'
        IN_PROGRESS = 'IN_PROGRESS', 'En cours'
        COMPLETED = 'COMPLETED', 'Terminée'
        CANCELLED = 'CANCELLED', 'Annulée'

    # ============================================
    # RELATIONS
    # ============================================

    # L'alerte associée à cette intervention
    alert = models.OneToOneField(
        'alerts.Alert',
        on_delete=models.CASCADE,
        related_name='intervention',
        help_text="L'alerte à laquelle cette intervention est associée"
    )

    # L'équipe assignée à cette intervention
    team = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_interventions',
        limit_choices_to={'role': 'INTERVENTION_TEAM'},
        help_text="L'équipe d'intervention assignée"
    )

    # La personne qui a créé cette intervention
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_interventions',
        help_text="L'autorité qui a créé cette intervention"
    )

    # ============================================
    # INFORMATIONS SUR L'INTERVENTION
    # ============================================

    # Titre de l'intervention
    title = models.CharField(
        max_length=200,
        help_text="Titre de l'intervention"
    )

    # Description détaillée
    description = models.TextField(
        help_text="Description détaillée de l'intervention"
    )

    # Statut actuel
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ASSIGNED,
        help_text="Statut actuel de l'intervention"
    )

    # ============================================
    # LOCALISATION
    # ============================================

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        help_text="Latitude du lieu d'intervention"
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        help_text="Longitude du lieu d'intervention"
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Adresse du lieu d'intervention"
    )

    # ============================================
    # MÉTADONNÉES
    # ============================================

    # Temps estimé d'arrivée (en minutes)
    estimated_arrival_minutes = models.IntegerField(
        null=True,
        blank=True,
        help_text="Temps estimé d'arrivée en minutes"
    )

    # Temps réel d'arrivée
    actual_arrival_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Heure réelle d'arrivée sur place"
    )

    # Temps de début d'intervention
    start_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Heure de début de l'intervention"
    )

    # Temps de fin d'intervention
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Heure de fin de l'intervention"
    )

    # Notes de l'équipe
    team_notes = models.TextField(
        blank=True,
        help_text="Notes prises par l'équipe pendant l'intervention"
    )

    # Résultat de l'intervention
    outcome = models.TextField(
        blank=True,
        help_text="Résultat de l'intervention"
    )

    # ============================================
    # TIMESTAMPS
    # ============================================

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    # ============================================
    # META CLASSE
    # ============================================

    class Meta:
        db_table = 'interventions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['team']),
            models.Index(fields=['alert']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['-created_at']),
        ]

    # ============================================
    # MÉTHODES
    # ============================================

    def __str__(self):
        return f"Intervention #{self.id} - {self.title} ({self.get_status_display()})"

    @property
    def duration_minutes(self):
        """Calculer la durée de l'intervention en minutes."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 60
        if self.start_time:
            return (timezone.now() - self.start_time).total_seconds() / 60
        return None

    @property
    def is_active(self):
        """Vérifier si l'intervention est active."""
        return self.status not in [self.Status.COMPLETED, self.Status.CANCELLED]

    def mark_as_en_route(self, estimated_arrival=None):
        """Marquer l'intervention comme 'En route'."""
        self.status = self.Status.EN_ROUTE
        if estimated_arrival:
            self.estimated_arrival_minutes = estimated_arrival
        self.save()
        return self

    def mark_as_on_site(self):
        """Marquer l'intervention comme 'Sur place'."""
        self.status = self.Status.ON_SITE
        self.actual_arrival_time = timezone.now()
        self.save()
        return self

    def mark_as_in_progress(self):
        """Marquer l'intervention comme 'En cours'."""
        self.status = self.Status.IN_PROGRESS
        if not self.start_time:
            self.start_time = timezone.now()
        self.save()
        return self

    def mark_as_completed(self, outcome=""):
        """Marquer l'intervention comme 'Terminée'."""
        self.status = self.Status.COMPLETED
        self.end_time = timezone.now()
        self.resolved_at = timezone.now()
        if outcome:
            self.outcome = outcome
        self.save()

        # Mettre à jour l'alerte associée
        if hasattr(self, 'alert'):
            self.alert.mark_as_resolved(self.created_by)

        return self

    def mark_as_cancelled(self, reason=""):
        """Marquer l'intervention comme 'Annulée'."""
        self.status = self.Status.CANCELLED
        if reason:
            self.team_notes = f"Annulée: {reason}"
        self.save()
        return self

    def add_note(self, note):
        """Ajouter une note à l'intervention."""
        if self.team_notes:
            self.team_notes = f"{self.team_notes}\n\n{timezone.now().strftime('%Y-%m-%d %H:%M')} - {note}"
        else:
            self.team_notes = f"{timezone.now().strftime('%Y-%m-%d %H:%M')} - {note}"
        self.save()
        return self


# ============================================
# MODÈLE 2: InterventionUpdate
# ============================================

class InterventionUpdate(models.Model):
    """
    Modèle pour les mises à jour en temps réel des interventions.

    Permet de suivre l'évolution d'une intervention étape par étape.
    """

    # ============================================
    # RELATIONS
    # ============================================

    intervention = models.ForeignKey(
        Intervention,
        on_delete=models.CASCADE,
        related_name='updates',
        help_text="L'intervention concernée"
    )

    # Qui a fait cette mise à jour ?
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='intervention_updates',
        help_text="La personne qui a fait cette mise à jour"
    )

    # ============================================
    # CONTENU DE LA MISE À JOUR
    # ============================================

    # Ancien statut
    old_status = models.CharField(
        max_length=20,
        choices=Intervention.Status.choices,
        help_text="Statut avant la mise à jour"
    )

    # Nouveau statut
    new_status = models.CharField(
        max_length=20,
        choices=Intervention.Status.choices,
        help_text="Statut après la mise à jour"
    )

    # Message de la mise à jour
    message = models.TextField(
        help_text="Description de la mise à jour"
    )

    # ============================================
    # TIMESTAMPS
    # ============================================

    created_at = models.DateTimeField(auto_now_add=True)

    # ============================================
    # META CLASSE
    # ============================================

    class Meta:
        db_table = 'intervention_updates'
        ordering = ['-created_at']

    def __str__(self):
        return f"Mise à jour #{self.id} - {self.get_new_status_display()}"