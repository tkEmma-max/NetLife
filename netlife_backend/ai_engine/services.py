# ai_engine/services.py
import os
import time
import json
import base64
import re
from django.conf import settings
from django.utils import timezone
from .models import AIAnalysis


class GeminiAIService:
    """Service pour interagir avec Google Gemini AI."""

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY', '')
        self.model = None
        self.vision_model = None

        try:
            import google.generativeai as genai
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-pro')
                self.vision_model = genai.GenerativeModel('gemini-1.5-pro')
        except ImportError:
            print("⚠️ Google Generative AI non installé.")

    def is_available(self):
        return self.model is not None and self.api_key

    def analyze_report(self, report):
        """Analyser un rapport avec Gemini AI."""
        if not self.is_available():
            return self._mock_analysis(report)

        try:
            # Pour le MVP, on utilise une analyse simulée
            return self._mock_analysis(report)
        except Exception as e:
            return self._handle_error(report, str(e))

    def _mock_analysis(self, report):
        """Analyse simulée pour les tests."""
        # Vérifier les mots-clés de blague
        joke_keywords = ['blague', 'test', 'prank', 'fun', 'lol', 'haha', 'rire']
        title_lower = report.title.lower()
        desc_lower = report.description.lower()

        for keyword in joke_keywords:
            if keyword in title_lower or keyword in desc_lower:
                return AIAnalysis.objects.create(
                    report=report,
                    is_valid_danger=False,
                    rejection_reason="Ceci semble être une blague ou un test. Veuillez signaler uniquement les vrais dangers.",
                    is_successful=True,
                    analyzed_at=timezone.now()
                )

        # Vérifier les mots-clés de danger réel
        danger_keywords = ['feu', 'incendie', 'fumée', 'inondation', 'déchet', 'pollution']
        for keyword in danger_keywords:
            if keyword in title_lower or keyword in desc_lower:
                return AIAnalysis.objects.create(
                    report=report,
                    danger_type='FIRE',
                    severity_score=8,
                    severity_level='HIGH',
                    confidence_score=85,
                    recommended_action='IMMEDIATE_EVACUATION',
                    advice='🚨 Feu détecté. Évacuation immédiate recommandée.',
                    safety_tips='Restez bas, couvrez-vous le nez, appelez le 118.',
                    emergency_contacts='Pompiers: 118, Police: 117, Ambulance: 119',
                    is_valid_danger=True,
                    is_successful=True,
                    analyzed_at=timezone.now()
                )

        # Si aucun danger n'est détecté
        return AIAnalysis.objects.create(
            report=report,
            is_valid_danger=False,
            rejection_reason="Aucun danger environnemental détecté dans ce rapport.",
            is_successful=True,
            analyzed_at=timezone.now()
        )

    def _handle_error(self, report, error_message):
        """Gérer les erreurs."""
        return AIAnalysis.objects.create(
            report=report,
            is_successful=False,
            is_valid_danger=False,
            error_message=error_message,
            analyzed_at=timezone.now()
        )