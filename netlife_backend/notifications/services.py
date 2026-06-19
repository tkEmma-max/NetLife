# notifications/services.py
# ============================================
# SERVICES POUR L'APPLICATION NOTIFICATIONS
# ============================================

from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Notification, FCMDevice


class NotificationService:
    """Service pour la gestion des notifications."""

    # ============================================
    # CRÉATION DE NOTIFICATIONS
    # ============================================

    def create_notification(self, recipient, notification_type, title, message,
                            channel='IN_APP', data=None, image_url='',
                            alert=None, intervention=None):
        """Créer une notification."""

        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            channel=channel,
            data=data or {},
            image_url=image_url,
            alert=alert,
            intervention=intervention
        )

        # Marquer comme envoyée selon le canal
        if channel != 'IN_APP':
            notification.mark_as_sent()

        # Envoyer la notification selon le canal
        self._send_notification(notification)

        return notification

    # ============================================
    # ENVOI DE NOTIFICATIONS
    # ============================================

    def _send_notification(self, notification):
        """Envoyer la notification selon le canal."""

        if notification.channel == 'PUSH':
            self._send_push_notification(notification)
        elif notification.channel == 'EMAIL':
            self._send_email_notification(notification)
        elif notification.channel == 'SMS':
            self._send_sms_notification(notification)

    def _send_push_notification(self, notification):
        """Envoyer une notification push via FCM."""

        # Récupérer les tokens FCM de l'utilisateur
        devices = FCMDevice.objects.filter(
            user=notification.recipient,
            is_active=True
        )

        if not devices.exists():
            print(f"⚠️ Aucun appareil FCM pour {notification.recipient.email}")
            return

        # Dans la vraie vie, on utiliserait firebase_admin
        # pour envoyer les notifications push
        # Pour le MVP, on simule l'envoi

        for device in devices:
            print(f"📲 Push notification envoyée à {device.fcm_token[:20]}...")
            print(f"   Titre: {notification.title}")
            print(f"   Message: {notification.message}")

        # Simuler l'envoi
        notification.mark_as_sent()

    def _send_email_notification(self, notification):
        """Envoyer une notification par email."""

        subject = notification.title
        message = notification.message

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.recipient.email],
                fail_silently=False,
            )
            notification.mark_as_sent()
            print(f"📧 Email envoyé à {notification.recipient.email}")
        except Exception as e:
            print(f"❌ Erreur d'envoi d'email: {e}")

    def _send_sms_notification(self, notification):
        """Envoyer une notification par SMS."""

        # Dans la vraie vie, on utiliserait une API SMS comme Twilio, Orange SMS, etc.
        # Pour le MVP, on simule l'envoi

        phone = notification.recipient.phone_number
        if phone:
            print(f"📱 SMS envoyé à {phone}")
            print(f"   Message: {notification.message}")
            notification.mark_as_sent()
        else:
            print(f"⚠️ Aucun numéro de téléphone pour {notification.recipient.email}")

    # ============================================
    # NOTIFICATIONS PAR TYPES
    # ============================================

    def send_alert_notification(self, alert, recipient):
        """Envoyer une notification d'alerte."""

        priority = alert.get_priority_display()
        danger_type = alert.get_danger_type_display()

        title = f"🚨 ALERTE {priority.upper()} - {danger_type}"
        message = f"{alert.title}\n📍 {alert.address or 'Voir la carte'}"

        data = {
            'type': 'ALERT',
            'alert_id': alert.id,
            'latitude': str(alert.latitude),
            'longitude': str(alert.longitude),
            'priority': alert.priority,
            'severity': alert.severity,
        }

        return self.create_notification(
            recipient=recipient,
            notification_type='ALERT',
            title=title,
            message=message,
            channel='PUSH',
            data=data,
            alert=alert
        )

    def send_intervention_update(self, intervention, recipient):
        """Envoyer une notification de mise à jour d'intervention."""

        status = intervention.get_status_display()
        title = f"🚒 Mise à jour intervention - {status}"
        message = f"{intervention.title}\nStatut: {status}"

        data = {
            'type': 'INTERVENTION',
            'intervention_id': intervention.id,
            'status': intervention.status,
        }

        return self.create_notification(
            recipient=recipient,
            notification_type='INTERVENTION',
            title=title,
            message=message,
            channel='PUSH',
            data=data,
            intervention=intervention
        )

    def send_points_notification(self, user, points, reason):
        """Envoyer une notification de points gagnés."""

        title = "🏆 Points gagnés !"
        message = f"Vous avez gagné {points} points !\nRaison: {reason}"

        data = {
            'type': 'POINTS',
            'points': points,
            'reason': reason,
        }

        return self.create_notification(
            recipient=user,
            notification_type='POINTS_AWARDED',
            title=title,
            message=message,
            channel='IN_APP',
            data=data
        )

    def send_report_verified_notification(self, report, recipient):
        """Envoyer une notification de rapport vérifié."""

        title = "✅ Votre rapport a été vérifié !"
        message = f"Votre rapport \"{report.title}\" a été vérifié par les autorités."

        data = {
            'type': 'REPORT_VERIFIED',
            'report_id': report.id,
        }

        return self.create_notification(
            recipient=recipient,
            notification_type='REPORT_VERIFIED',
            title=title,
            message=message,
            channel='IN_APP',
            data=data,
            alert=report.alert if hasattr(report, 'alert') else None
        )

    # ============================================
    # MÉTHODES UTILITAIRES
    # ============================================

    def get_unread_count(self, user):
        """Compter les notifications non lues d'un utilisateur."""
        return Notification.objects.filter(
            recipient=user,
            is_read=False
        ).count()

    def mark_all_as_read(self, user):
        """Marquer toutes les notifications d'un utilisateur comme lues."""
        count = Notification.objects.filter(
            recipient=user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return count

    def broadcast_alert(self, alert, recipients):
        """Diffuser une alerte à plusieurs utilisateurs."""

        notifications = []
        for recipient in recipients:
            try:
                notif = self.send_alert_notification(alert, recipient)
                notifications.append(notif)
            except Exception as e:
                print(f"❌ Erreur pour {recipient.email}: {e}")

        return notifications