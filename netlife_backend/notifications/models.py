from django.db import models

# Create your models here.
# notifications/models.py
# ============================================
# MODÈLES POUR L'APPLICATION NOTIFICATIONS
# ============================================

from django.db import models
from django.conf import settings
from django.utils import timezone


class Notification(models.Model):
    """
    Modèle principal pour les notifications.

    Stocke toutes les notifications envoyées aux utilisateurs.
    """

    # ============================================
    # TYPES DE NOTIFICATIONS
    # ============================================

    class NotificationType(models.TextChoices):
        ALERT = 'ALERT', 'Alerte d\'urgence'
        INTERVENTION = 'INTERVENTION', 'Mise à jour intervention'
        REPORT_VERIFIED = 'REPORT_VERIFIED', 'Rapport vérifié'
        POINTS_AWARDED = 'POINTS_AWARDED', 'Points gagnés'
        POINTS_REDEEMED = 'POINTS_REDEEMED', 'Points échangés'
        STATUS_UPDATE = 'STATUS_UPDATE', 'Mise à jour statut'
        RESOLVED = 'RESOLVED', 'Résolu'
        SYSTEM = 'SYSTEM', 'Notification système'

    # ============================================
    # CANAUX D'ENVOI
    # ============================================

    class Channel(models.TextChoices):
        PUSH = 'PUSH', 'Push Notification'
        EMAIL = 'EMAIL', 'Email'
        SMS = 'SMS', 'SMS'
        IN_APP = 'IN_APP', 'In-App'

    # ============================================
    # RELATIONS
    # ============================================

    # À qui est envoyée la notification ?
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="L'utilisateur qui reçoit la notification"
    )

    # Quelle alerte a déclenché cette notification ?
    alert = models.ForeignKey(
        'alerts.Alert',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications',
        help_text="L'alerte associée à cette notification"
    )

    # Quelle intervention est concernée ?
    intervention = models.ForeignKey(
        'interventions.Intervention',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications',
        help_text="L'intervention associée à cette notification"
    )

    # ============================================
    # CONTENU DE LA NOTIFICATION
    # ============================================

    # Type de notification
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        help_text="Type de notification"
    )

    # Titre de la notification
    title = models.CharField(
        max_length=200,
        help_text="Titre de la notification"
    )

    # Message de la notification
    message = models.TextField(
        help_text="Message de la notification"
    )

    # Canal d'envoi
    channel = models.CharField(
        max_length=10,
        choices=Channel.choices,
        default=Channel.IN_APP,
        help_text="Canal d'envoi de la notification"
    )

    # ============================================
    # DONNÉES SUPPLÉMENTAIRES (pour le frontend)
    # ============================================

    # Données JSON pour action (ex: ouvrir un écran spécifique)
    data = models.JSONField(
        default=dict,
        help_text="Données supplémentaires pour le frontend"
    )

    # URL de l'image (si applicable)
    image_url = models.URLField(
        blank=True,
        help_text="URL de l'image associée à la notification"
    )

    # ============================================
    # STATUT DE LA NOTIFICATION
    # ============================================

    # La notification a-t-elle été lue ?
    is_read = models.BooleanField(
        default=False,
        help_text="La notification a-t-elle été lue ?"
    )

    # La notification a-t-elle été envoyée avec succès ?
    is_sent = models.BooleanField(
        default=False,
        help_text="La notification a-t-elle été envoyée ?"
    )

    # Date de lecture
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date de lecture de la notification"
    )

    # Date d'envoi
    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date d'envoi de la notification"
    )

    # ============================================
    # TIMESTAMPS
    # ============================================

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ============================================
    # META CLASSE
    # ============================================

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient']),
            models.Index(fields=['is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['-created_at']),
        ]

    # ============================================
    # MÉTHODES
    # ============================================

    def __str__(self):
        return f"Notification #{self.id} - {self.title[:50]}"

    def mark_as_read(self):
        """Marquer la notification comme lue."""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
        return self

    def mark_as_sent(self):
        """Marquer la notification comme envoyée."""
        if not self.is_sent:
            self.is_sent = True
            self.sent_at = timezone.now()
            self.save()
        return self


# ============================================
# MODÈLE 2: FCMDevice (pour push notifications)
# ============================================

class FCMDevice(models.Model):
    """
    Modèle pour stocker les tokens FCM des appareils.

    Permet d'envoyer des push notifications aux appareils mobiles.
    """

    # ============================================
    # RELATIONS
    # ============================================

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fcm_devices',
        help_text="L'utilisateur propriétaire de l'appareil"
    )

    # ============================================
    # INFORMATIONS DE L'APPAREIL
    # ============================================

    # Token FCM (Firebase Cloud Messaging)
    fcm_token = models.CharField(
        max_length=255,
        unique=True,
        help_text="Token FCM de l'appareil"
    )

    # Type d'appareil
    device_type = models.CharField(
        max_length=10,
        choices=[('ANDROID', 'Android'), ('IOS', 'iOS'), ('WEB', 'Web')],
        default='ANDROID',
        help_text="Type d'appareil"
    )

    # ============================================
    # STATUT
    # ============================================

    is_active = models.BooleanField(
        default=True,
        help_text="L'appareil est-il actif ?"
    )

    # ============================================
    # TIMESTAMPS
    # ============================================

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ============================================
    # META CLASSE
    # ============================================

    class Meta:
        db_table = 'fcm_devices'
        ordering = ['-created_at']
        unique_together = ['user', 'fcm_token']

    def __str__(self):
        return f"{self.user.email} - {self.fcm_token[:20]}..."