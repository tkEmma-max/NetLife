# reports/services.py
# ============================================
# EXPLANATION: Business logic for reports
# Handles AI analysis, GPS validation, etc.
# ============================================

from django.core.exceptions import ValidationError
from .models import Report


class ReportService:
    """
    Service class for report business logic.

    Purpose: To handle complex operations that don't belong in views
    """

    @staticmethod
    def trigger_ai_analysis(report):
        """
        Send report to Gemini AI for analysis.

        This will be implemented when we build the ai_engine app.
        For now, it's a placeholder.
        """
        # TODO: Send to Gemini AI
        # For now, just return a mock analysis
        print(f"AI Analysis triggered for report #{report.id}")
        return {
            'danger_type': 'FIRE',
            'severity': 8,
            'confidence': 85
        }

    @staticmethod
    def validate_gps_location(latitude, longitude):
        """
        Validate GPS coordinates.

        Purpose: Ensure coordinates are in Cameroon region
        """
        try:
            lat = float(latitude)
            lng = float(longitude)
        except (TypeError, ValueError):
            raise ValidationError("Invalid GPS coordinates")

        # Cameroon bounding box (approximate)
        if not (2 <= lat <= 13):
            raise ValidationError("Latitude not in Cameroon region")

        if not (8 <= lng <= 16):
            raise ValidationError("Longitude not in Cameroon region")

        return True

    @staticmethod
    def calculate_severity(danger_type, confidence):
        """
        Calculate severity based on danger type and confidence.

        Purpose: To determine how urgent the alert should be
        """
        severity_map = {
            'FIRE': 9,
            'FLOOD': 8,
            'POLLUTION': 6,
            'DEFORESTATION': 5,
            'WASTE': 4,
            'ROAD_HAZARD': 7,
            'OTHER': 5
        }

        base_severity = severity_map.get(danger_type, 5)

        if confidence > 90:
            return min(10, base_severity + 1)
        elif confidence > 70:
            return base_severity
        else:
            return max(1, base_severity - 1)