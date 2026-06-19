# notifications/urls.py
# ============================================
# ROUTAGE POUR L'APPLICATION NOTIFICATIONS
# ============================================

from django.urls import path
from . import views

urlpatterns = [
    # Liste des notifications
    path('', views.NotificationListView.as_view(), name='notification-list'),

    # Détails d'une notification
    path('<int:notification_id>/', views.NotificationDetailView.as_view(), name='notification-detail'),

    # Marquer une notification comme lue
    path('<int:notification_id>/read/', views.MarkNotificationReadView.as_view(), name='mark-read'),

    # Marquer toutes les notifications comme lues
    path('mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='mark-all-read'),

    # Nombre de notifications non lues
    path('unread-count/', views.UnreadCountView.as_view(), name='unread-count'),

    # Enregistrement FCM
    path('register-device/', views.FCMDeviceRegisterView.as_view(), name='register-device'),

    # Désenregistrement FCM
    path('unregister-device/', views.FCMDeviceUnregisterView.as_view(), name='unregister-device'),
]