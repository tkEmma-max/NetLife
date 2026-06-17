# interventions/serializers.py
# ============================================
# SERIALIZERS POUR L'APPLICATION INTERVENTIONS
# ============================================

from rest_framework import serializers
from .models import Intervention, InterventionUpdate
from alerts.serializers import AlertSerializer


class InterventionUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour les mises à jour d'intervention."""

    updated_by_email = serializers.EmailField(source='updated_by.email', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.username', read_only=True)
    old_status_display = serializers.CharField(source='get_old_status_display', read_only=True)
    new_status_display = serializers.CharField(source='get_new_status_display', read_only=True)

    class Meta:
        model = InterventionUpdate
        fields = [
            'id',
            'intervention',
            'updated_by',
            'updated_by_email',
            'updated_by_name',
            'old_status',
            'old_status_display',
            'new_status',
            'new_status_display',
            'message',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class InterventionSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Intervention."""

    # Affichages lisibles
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    # Données de l'alerte associée
    alert_data = AlertSerializer(source='alert', read_only=True)

    # Informations sur l'équipe
    team_name = serializers.CharField(source='team.username', read_only=True)
    team_email = serializers.EmailField(source='team.email', read_only=True)

    # Informations sur le créateur
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)

    # Propriétés calculées
    duration_minutes = serializers.FloatField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    # Mises à jour (nested)
    updates = InterventionUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Intervention
        fields = [
            'id',
            'alert',
            'alert_data',
            'team',
            'team_name',
            'team_email',
            'created_by',
            'created_by_name',
            'created_by_email',
            'title',
            'description',
            'status',
            'status_display',
            'latitude',
            'longitude',
            'address',
            'estimated_arrival_minutes',
            'actual_arrival_time',
            'start_time',
            'end_time',
            'team_notes',
            'outcome',
            'duration_minutes',
            'is_active',
            'updates',
            'created_at',
            'updated_at',
            'resolved_at',
        ]
        read_only_fields = [
            'id',
            'created_by',
            'created_at',
            'updated_at',
            'resolved_at',
            'duration_minutes',
            'is_active',
            'updates',
        ]


class InterventionCreateSerializer(serializers.Serializer):
    """Serializer pour la création d'une intervention."""

    alert_id = serializers.IntegerField(required=True)
    team_id = serializers.IntegerField(required=True)
    estimated_arrival = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_alert_id(self, value):
        """Vérifier que l'alerte existe et n'a pas déjà une intervention."""
        from alerts.models import Alert
        try:
            alert = Alert.objects.get(id=value)
            if hasattr(alert, 'intervention'):
                raise serializers.ValidationError(
                    "Cette alerte a déjà une intervention."
                )
        except Alert.DoesNotExist:
            raise serializers.ValidationError("Alerte introuvable.")
        return value

    def validate_team_id(self, value):
        """Vérifier que l'équipe existe et a le bon rôle."""
        from accounts.models import User
        try:
            team = User.objects.get(id=value)
            if team.role != 'INTERVENTION_TEAM':
                raise serializers.ValidationError(
                    "Cet utilisateur n'est pas une équipe d'intervention."
                )
        except User.DoesNotExist:
            raise serializers.ValidationError("Équipe introuvable.")
        return value


class InterventionStatusUpdateSerializer(serializers.Serializer):
    """Serializer pour la mise à jour du statut."""

    status = serializers.ChoiceField(
        choices=Intervention.Status.choices,
        required=True,
        help_text="Nouveau statut de l'intervention"
    )
    message = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Message optionnel pour la mise à jour"
    )
    outcome = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Résultat de l'intervention (si terminée)"
    )