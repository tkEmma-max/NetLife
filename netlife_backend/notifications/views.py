from django.shortcuts import render

# Create your views here.
# notifications/views.py
# ============================================
# VUES POUR L'APPLICATION NOTIFICATIONS
# ============================================

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Notification, FCMDevice
from .serializers import NotificationSerializer, FCMDeviceSerializer
from .services import NotificationService


class NotificationListView(APIView):
    """
    API pour lister les notifications de l'utilisateur connecté.

    UTILISATION:
        GET /api/notifications/
        GET /api/notifications/?unread_only=true
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user)

        # Filtrer les notifications non lues
        if request.query_params.get('unread_only') == 'true':
            notifications = notifications.filter(is_read=False)

        notifications = notifications.order_by('-created_at')

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class NotificationDetailView(APIView):
    """
    API pour récupérer une notification spécifique.

    UTILISATION:
        GET /api/notifications/{id}/
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)

        # Vérifier que l'utilisateur est le propriétaire
        if notification.recipient != request.user:
            return Response(
                {'error': 'Vous n\'avez pas la permission de voir cette notification.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = NotificationSerializer(notification)
        return Response(serializer.data)


class MarkNotificationReadView(APIView):
    """
    API pour marquer une notification comme lue.

    UTILISATION:
        POST /api/notifications/{id}/read/
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)

        if notification.recipient != request.user:
            return Response(
                {'error': 'Vous n\'avez pas la permission de modifier cette notification.'},
                status=status.HTTP_403_FORBIDDEN
            )

        notification.mark_as_read()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)


class MarkAllNotificationsReadView(APIView):
    """
    API pour marquer toutes les notifications comme lues.

    UTILISATION:
        POST /api/notifications/mark-all-read/
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        service = NotificationService()
        count = service.mark_all_as_read(request.user)
        return Response({
            'message': f'{count} notifications marquées comme lues.'
        })


class UnreadCountView(APIView):
    """
    API pour obtenir le nombre de notifications non lues.

    UTILISATION:
        GET /api/notifications/unread-count/
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        service = NotificationService()
        count = service.get_unread_count(request.user)
        return Response({'unread_count': count})


class FCMDeviceRegisterView(APIView):
    """
    API pour enregistrer un token FCM pour les push notifications.

    UTILISATION:
        POST /api/notifications/register-device/
        {
            "fcm_token": "token_du_periphérique",
            "device_type": "ANDROID"
        }
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        fcm_token = request.data.get('fcm_token')
        device_type = request.data.get('device_type', 'ANDROID')

        if not fcm_token:
            return Response(
                {'error': 'fcm_token est requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier si le token existe déjà
        device, created = FCMDevice.objects.get_or_create(
            user=request.user,
            fcm_token=fcm_token,
            defaults={'device_type': device_type}
        )

        if not created:
            device.is_active = True
            device.save()

        serializer = FCMDeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FCMDeviceUnregisterView(APIView):
    """
    API pour désenregistrer un token FCM.

    UTILISATION:
        DELETE /api/notifications/unregister-device/
        {
            "fcm_token": "token_du_periphérique"
        }
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        fcm_token = request.data.get('fcm_token')

        if not fcm_token:
            return Response(
                {'error': 'fcm_token est requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            device = FCMDevice.objects.get(
                user=request.user,
                fcm_token=fcm_token
            )
            device.delete()
            return Response(
                {'message': 'Appareil désenregistré avec succès.'},
                status=status.HTTP_200_OK
            )
        except FCMDevice.DoesNotExist:
            return Response(
                {'error': 'Token non trouvé.'},
                status=status.HTTP_404_NOT_FOUND
            )