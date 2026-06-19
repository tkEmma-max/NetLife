from django.shortcuts import render

# Create your views here.
# interventions/views.py
# ============================================
# VUES POUR L'APPLICATION INTERVENTIONS
# ============================================

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Intervention, InterventionUpdate
from .serializers import (
    InterventionSerializer,
    InterventionCreateSerializer,
    InterventionStatusUpdateSerializer,
    InterventionUpdateSerializer
)
from .services import InterventionService
from alerts.models import Alert


class CreateInterventionView(APIView):
    """
    API pour créer une intervention à partir d'une alerte.

    UTILISATION:
        POST /api/interventions/create/
        {
            "alert_id": 1,
            "team_id": 5,
            "estimated_arrival": 15,
            "notes": "Équipe envoyée"
        }
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Vérifier que l'utilisateur est une autorité
        if not (request.user.is_authority or request.user.is_admin):
            return Response(
                {'error': 'Seules les autorités peuvent créer des interventions.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Valider les données
        serializer = InterventionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Créer l'intervention
        service = InterventionService()
        try:
            intervention = service.create_intervention(
                alert_id=serializer.validated_data['alert_id'],
                team_id=serializer.validated_data['team_id'],
                created_by=request.user,
                notes=serializer.validated_data.get('notes', '')
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retourner l'intervention créée
        response_serializer = InterventionSerializer(
            intervention,
            context={'request': request}
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ActiveInterventionsView(ListAPIView):
    """
    API pour récupérer toutes les interventions actives.

    UTILISATION:
        GET /api/interventions/active/
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InterventionSerializer

    def get_queryset(self):
        return Intervention.objects.filter(
            status__in=[
                Intervention.Status.ASSIGNED,
                Intervention.Status.EN_ROUTE,
                Intervention.Status.ON_SITE,
                Intervention.Status.IN_PROGRESS
            ]
        ).order_by('-created_at')


class InterventionDetailView(APIView):
    """
    API pour récupérer les détails d'une intervention.

    UTILISATION:
        GET /api/interventions/{id}/
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, intervention_id):
        intervention = get_object_or_404(Intervention, id=intervention_id)

        # Vérifier les permissions
        user = request.user
        if not (user.is_authority or user.is_admin or intervention.team == user):
            return Response(
                {'error': 'Vous n\'avez pas la permission de voir cette intervention.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = InterventionSerializer(intervention, context={'request': request})
        return Response(serializer.data)


class UpdateInterventionStatusView(APIView):
    """
    API pour mettre à jour le statut d'une intervention.

    UTILISATION:
        PATCH /api/interventions/{id}/status/
        {
            "status": "EN_ROUTE",
            "message": "Équipe en route vers le lieu"
        }
    """

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, intervention_id):
        intervention = get_object_or_404(Intervention, id=intervention_id)

        # Vérifier les permissions
        user = request.user
        if not (user.is_authority or user.is_admin or intervention.team == user):
            return Response(
                {'error': 'Vous n\'avez pas la permission de modifier cette intervention.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Valider les données
        serializer = InterventionStatusUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Mettre à jour le statut
        service = InterventionService()
        intervention = service.update_status(
            intervention=intervention,
            new_status=serializer.validated_data['status'],
            updated_by=user,
            message=serializer.validated_data.get('message', '')
        )

        # Si terminée, ajouter le résultat
        if 'outcome' in serializer.validated_data:
            intervention.outcome = serializer.validated_data['outcome']
            intervention.save()

        # Retourner l'intervention mise à jour
        response_serializer = InterventionSerializer(
            intervention,
            context={'request': request}
        )
        return Response(response_serializer.data)


class InterventionUpdatesView(APIView):
    """
    API pour récupérer toutes les mises à jour d'une intervention.

    UTILISATION:
        GET /api/interventions/{id}/updates/
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, intervention_id):
        intervention = get_object_or_404(Intervention, id=intervention_id)

        # Vérifier les permissions
        user = request.user
        if not (user.is_authority or user.is_admin or intervention.team == user):
            return Response(
                {'error': 'Vous n\'avez pas la permission de voir ces mises à jour.'},
                status=status.HTTP_403_FORBIDDEN
            )

        updates = intervention.updates.all().order_by('-created_at')
        serializer = InterventionUpdateSerializer(updates, many=True)
        return Response(serializer.data)


class TeamInterventionsView(ListAPIView):
    """
    API pour récupérer toutes les interventions d'une équipe.

    UTILISATION:
        GET /api/interventions/team/{team_id}/
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InterventionSerializer

    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        user = self.request.user

        # Vérifier les permissions
        if not (user.is_authority or user.is_admin or user.id == int(team_id)):
            return Intervention.objects.none()

        return Intervention.objects.filter(team_id=team_id).order_by('-created_at')


class AddNoteView(APIView):
    """
    API pour ajouter une note à une intervention.

    UTILISATION:
        POST /api/interventions/{id}/add-note/
        {
            "note": "Nouvelle note sur l'intervention"
        }
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, intervention_id):
        intervention = get_object_or_404(Intervention, id=intervention_id)

        # Vérifier les permissions
        user = request.user
        if not (user.is_authority or user.is_admin or intervention.team == user):
            return Response(
                {'error': 'Vous n\'avez pas la permission d\'ajouter des notes.'},
                status=status.HTTP_403_FORBIDDEN
            )

        note = request.data.get('note')
        if not note:
            return Response(
                {'error': 'La note est requise.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        intervention.add_note(note)

        serializer = InterventionSerializer(intervention, context={'request': request})
        return Response(serializer.data)