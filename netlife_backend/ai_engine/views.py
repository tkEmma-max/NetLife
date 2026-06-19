# ai_engine/views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from reports.models import Report
from .models import AIAnalysis
from .serializers import AIAnalysisSerializer
from .services import GeminiAIService


class AnalyzeReportView(APIView):
    """Analyser un rapport avec l'IA."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, report_id):
        if not (request.user.is_authority or request.user.is_admin):
            return Response(
                {'error': 'Seules les autorités peuvent déclencher l\'analyse IA.'},
                status=status.HTTP_403_FORBIDDEN
            )

        report = get_object_or_404(Report, id=report_id)

        if hasattr(report, 'ai_analysis'):
            return Response(
                {'error': 'Ce rapport a déjà été analysé.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ai_service = GeminiAIService()
        analysis = ai_service.analyze_report(report)

        serializer = AIAnalysisSerializer(analysis, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAnalysisView(APIView):
    """Obtenir l'analyse IA d'un rapport."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, report_id):
        report = get_object_or_404(Report, id=report_id)

        if not (request.user.is_authority or request.user.is_admin or report.reporter == request.user):
            return Response(
                {'error': 'Vous n\'avez pas la permission de voir cette analyse.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            analysis = AIAnalysis.objects.get(report=report)
            serializer = AIAnalysisSerializer(analysis, context={'request': request})
            return Response(serializer.data)
        except AIAnalysis.DoesNotExist:
            return Response(
                {'error': 'Analyse non trouvée pour ce rapport.'},
                status=status.HTTP_404_NOT_FOUND
            )