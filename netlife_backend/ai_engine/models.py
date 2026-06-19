# ai_engine/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class AIAnalysis(models.Model):
    """Stocke les résultats d'analyse IA pour un rapport."""

    class DangerType(models.TextChoices):
        FIRE = 'FIRE', 'Feu'
        FLOOD = 'FLOOD', 'Inondation'
        WASTE = 'WASTE', 'Déchet illégal'
        DEFORESTATION = 'DEFORESTATION', 'Déforestation'
        POLLUTION = 'POLLUTION', 'Pollution'
        ROAD_HAZARD = 'ROAD_HAZARD', 'Danger routier'
        OTHER = 'OTHER', 'Autre'

    class SeverityLevel(models.TextChoices):
        LOW = 'LOW', 'Faible'
        MEDIUM = 'MEDIUM', 'Moyen'
        HIGH = 'HIGH', 'Élevé'
        CRITICAL = 'CRITICAL', 'Critique'

    class RecommendedAction(models.TextChoices):
        IMMEDIATE_EVACUATION = 'IMMEDIATE_EVACUATION', 'Évacuation immédiate'
        CALL_FIRE_DEPARTMENT = 'CALL_FIRE_DEPARTMENT', 'Appeler les pompiers'
        CALL_POLICE = 'CALL_POLICE', 'Appeler la police'
        CALL_AMBULANCE = 'CALL_AMBULANCE', 'Appeler une ambulance'
        AVOID_AREA = 'AVOID_AREA', 'Éviter la zone'
        MONITOR_SITUATION = 'MONITOR_SITUATION', 'Surveiller la situation'
        CONTACT_AUTHORITIES = 'CONTACT_AUTHORITIES', 'Contacter les autorités'
        NO_ACTION = 'NO_ACTION', 'Aucune action requise'

    report = models.OneToOneField(
        'reports.Report',
        on_delete=models.CASCADE,
        related_name='ai_analysis'
    )

    danger_type = models.CharField(
        max_length=20,
        choices=DangerType.choices,
        null=True,
        blank=True
    )

    severity_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    severity_level = models.CharField(
        max_length=10,
        choices=SeverityLevel.choices,
        null=True,
        blank=True
    )

    confidence_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    recommended_action = models.CharField(
        max_length=30,
        choices=RecommendedAction.choices,
        null=True,
        blank=True
    )

    advice = models.TextField(blank=True)
    safety_tips = models.TextField(blank=True)
    emergency_contacts = models.TextField(blank=True)

    is_valid_danger = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True)

    is_successful = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)

    analyzed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ai_analyses'
        ordering = ['-created_at']

    def __str__(self):
        return f"Analyse IA pour le Rapport #{self.report.id}"