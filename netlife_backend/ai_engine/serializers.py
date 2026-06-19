# ai_engine/serializers.py
from rest_framework import serializers
from .models import AIAnalysis


class AIAnalysisSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle AIAnalysis."""

    danger_type_display = serializers.CharField(
        source='get_danger_type_display',
        read_only=True
    )
    severity_level_display = serializers.CharField(
        source='get_severity_level_display',
        read_only=True
    )
    recommended_action_display = serializers.CharField(
        source='get_recommended_action_display',
        read_only=True
    )

    class Meta:
        model = AIAnalysis
        fields = [
            'id',
            'report',
            'danger_type',
            'danger_type_display',
            'severity_score',
            'severity_level',
            'severity_level_display',
            'confidence_score',
            'recommended_action',
            'recommended_action_display',
            'advice',
            'safety_tips',
            'emergency_contacts',
            'is_valid_danger',
            'rejection_reason',
            'analyzed_at',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'analyzed_at']