# reports/views.py
# ============================================
# EXPLANATION: This file contains ALL the logic for reports
# Each view handles one specific action
# Purpose: To process requests and return responses
# ============================================

from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from .models import Report, ReportEvidence, CrowdVerification
from .serializers import (
    ReportSerializer,
    ReportCreateSerializer,
    ReportEvidenceSerializer,
    ReportNearbySerializer,
    ReportStatusUpdateSerializer,
    CrowdVerificationSerializer
)
from .services import ReportService  # We'll create this next
from .utils import handle_evidence_upload  # We'll create this next

# ============================================
# IMPORTANT: Add this import at the top!
# ============================================
import os
import mimetypes
from math import radians, sin, cos, sqrt, atan2


# ============================================
# VIEW 1: ReportCreateView
# Handles SUBMITTING a new report (CITIZENS only)
# ============================================

class ReportCreateView(generics.CreateAPIView):
    """
    API endpoint for citizens to submit a new report.

    WHO: Citizens (authenticated users)
    WHAT: Creates a new report with evidence
    HOW: POST to /api/reports/submit/

    Flutter sends (multipart/form-data):
    {
        "title": "Fire at Mokolo Market",
        "description": "Large fire near the main market",
        "latitude": 4.0514,
        "longitude": 9.7019,
        "address": "Mokolo Market, Douala",
        "evidence": [file1.jpg, file2.mp4]
    }

    Returns: Created report data
    """

    # Only authenticated users can submit reports
    permission_classes = [permissions.IsAuthenticated]

    # This view handles file uploads
    parser_classes = [MultiPartParser, FormParser]

    # Use the create serializer
    serializer_class = ReportCreateSerializer

    def perform_create(self, serializer):
        """
        Override the default create behavior.

        Purpose: To handle evidence files separately
        Called after serializer validates the data
        """

        # Get the current user (who is submitting)
        user = self.request.user

        # Check if user is a citizen
        if not user.is_citizen:
            raise serializers.ValidationError(
                "Only citizens can submit reports."
            )

        # Get the validated data from the serializer
        validated_data = serializer.validated_data

        # Extract evidence files (handled separately)
        evidence_files = validated_data.pop('evidence', [])

        # Create the report with the remaining data
        # Set the reporter to the current user
        report = Report.objects.create(
            reporter=user,
            title=validated_data['title'],
            description=validated_data['description'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            address=validated_data.get('address', ''),
            gps_accuracy=validated_data.get('gps_accuracy'),
            status=Report.Status.PENDING_AI_ANALYSIS
        )

        # Handle each evidence file
        for file in evidence_files:
            self._handle_evidence(report, file)

        # Award initial points for submitting (10 points)
        user.add_points(10, f"Submitted report #{report.id}")

        # TODO: Trigger AI analysis (we'll do this later)
        # self.trigger_ai_analysis(report)

        # Store the created report in the serializer context
        # so the response includes it
        serializer.instance = report

        # Add the evidence to the response
        serializer.context['evidence'] = report.evidence.all()

    def _handle_evidence(self, report, file):
        """
        Helper method to handle a single evidence file.

        Purpose: To save the file and determine its type
        """

        # Get file extension
        filename = file.name
        ext = os.path.splitext(filename)[1].lower()

        # Determine evidence type
        if ext in ['.jpg', '.jpeg', '.png']:
            evidence_type = ReportEvidence.EvidenceType.IMAGE
        elif ext in ['.mp4', '.mov']:
            evidence_type = ReportEvidence.EvidenceType.VIDEO
        elif ext in ['.mp3', '.wav']:
            evidence_type = ReportEvidence.EvidenceType.AUDIO
        else:
            raise serializers.ValidationError(
                f"Unsupported file type: {ext}"
            )

        # Get MIME type
        mime_type = mimetypes.guess_type(filename)[0] or ''

        # Create the evidence record
        evidence = ReportEvidence.objects.create(
            report=report,
            file=file,
            evidence_type=evidence_type,
            original_filename=filename,
            mime_type=mime_type,
            file_size=file.size
        )

        return evidence

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle file uploads properly.

        Purpose: To return a custom response with report data
        """

        # Use the serializer to validate the data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Perform the create (calls perform_create above)
        self.perform_create(serializer)

        # Get the created report
        report = serializer.instance

        # Use the full ReportSerializer for the response
        response_serializer = ReportSerializer(
            report,
            context={'request': request}
        )

        # Return the response
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


# ============================================
# VIEW 2: ReportListView
# Lists reports for the current user (CITIZENS)
# ============================================

class ReportListView(generics.ListAPIView):
    """
    API endpoint for citizens to view their reports.

    WHO: Citizens (authenticated users)
    WHAT: List all reports submitted by the current user
    HOW: GET to /api/reports/my-reports/

    Returns: List of reports (paginated)
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReportSerializer
    pagination_class = None  # For MVP, we'll skip pagination

    def get_queryset(self):
        """
        Get reports for the current user.

        Purpose: Only show reports submitted by the logged-in user
        """
        user = self.request.user
        return Report.objects.filter(reporter=user).order_by('-created_at')


# ============================================
# VIEW 3: ReportDetailView
# Shows details of a SINGLE report
# ============================================

class ReportDetailView(generics.RetrieveAPIView):
    """
    API endpoint to view a specific report.

    WHO: Anyone (but data is filtered)
    WHAT: Get details of one report by ID
    HOW: GET to /api/reports/{id}/

    Returns: Full report data
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReportSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """
        Filter reports based on user role.

        Purpose: 
        - Citizens: Only see their own reports
        - Authorities: See all reports in their zone
        - Teams: See reports assigned to them
        """
        user = self.request.user

        if user.is_authority or user.is_admin:
            # Authorities and admins see all reports
            return Report.objects.all()

        elif user.is_intervention_team:
            # Teams only see reports in their zone
            return Report.objects.filter(
                Q(address__icontains=user.assigned_zone) |
                Q(crowd_verification_responses__citizen=user)
            )

        else:
            # Citizens only see their own reports
            return Report.objects.filter(reporter=user)


# ============================================
# VIEW 4: ReportNearbyView
# Lists reports NEAR a user's location
# ============================================

class ReportNearbyView(generics.ListAPIView):
    """
    API endpoint to find reports near a user's location.

    WHO: Everyone (authenticated)
    WHAT: Reports within a radius (default 5km)
    HOW: GET to /api/reports/nearby/?latitude=4.0514&longitude=9.7019&radius=5

    Returns: Simplified report list with distances
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReportNearbySerializer

    def get_queryset(self):
        """
        Get reports near the user's location.

        Purpose: Show citizens what's happening around them
        """

        # Get location from query parameters
        lat = self.request.query_params.get('latitude')
        lng = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius', 5)  # Default 5km

        if not lat or not lng:
            return Report.objects.none()

        try:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)
        except ValueError:
            return Report.objects.none()

        # Get all active reports (not rejected or resolved)
        reports = Report.objects.filter(
            is_active=True
        ).exclude(
            status__in=[Report.Status.REJECTED, Report.Status.RESOLVED]
        )

        # Filter by distance
        nearby_reports = []
        for report in reports:
            distance = self._calculate_distance(
                lat, lng,
                float(report.latitude),
                float(report.longitude)
            )

            if distance <= radius:
                # Add the distance to the report object
                report.distance = distance
                nearby_reports.append(report)

        # Sort by distance (closest first)
        nearby_reports.sort(key=lambda x: x.distance)

        return nearby_reports

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate distance between two GPS coordinates.

        Purpose: Using Haversine formula for accurate distance
        Returns: Distance in kilometers
        """

        # Convert to radians
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)

        # Haversine formula
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Earth's radius in kilometers
        R = 6371
        distance = R * c

        return distance


# ============================================
# VIEW 5: ReportStatusUpdateView
# Updates report status (AUTHORITIES only)
# ============================================

class ReportStatusUpdateView(APIView):
    """
    API endpoint for authorities to update report status.

    WHO: Authorities only
    WHAT: Verify, reject, or flag reports
    HOW: PATCH to /api/reports/{id}/status/

    Flutter sends:
    {
        "status": "VERIFIED",
        "comment": "I confirm this is a fire"
    }

    Returns: Updated report data
    """

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, report_id):
        """
        Handle status update.
        """

        # Check if user is authority
        user = request.user
        if not (user.is_authority or user.is_admin):
            return Response(
                {"error": "Only authorities can update report status."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get the report
        report = get_object_or_404(Report, id=report_id)

        # Validate the data
        serializer = ReportStatusUpdateSerializer(
            data=request.data,
            context={'report': report}
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the new status
        new_status = serializer.validated_data['status']
        comment = serializer.validated_data.get('comment', '')

        # Update the report status
        report.status = new_status

        # Additional actions based on status
        if new_status == 'VERIFIED':
            report.is_verified = True
            report.verified_by = user
            report.verified_at = timezone.now()

            # Award points to reporter
            # TODO: Calculate points based on severity
            points_awarded = 50  # Base points for verification
            report.award_points(points_awarded)

        elif new_status == 'ALERT_CREATED':
            # An alert will be created by the alerts app
            pass

        elif new_status == 'RESOLVED':
            report.resolved_at = timezone.now()

        report.save()

        # Return the updated report
        response_serializer = ReportSerializer(
            report,
            context={'request': request}
        )

        return Response(response_serializer.data)


# ============================================
# VIEW 6: AddEvidenceView
# Adds more evidence to an existing report
# ============================================

class AddEvidenceView(APIView):
    """
    API endpoint to add more evidence to a report.

    WHO: The reporter (citizen who created the report)
    WHAT: Upload additional evidence
    HOW: POST to /api/reports/{id}/add-evidence/

    Flutter sends (multipart/form-data):
    {
        "evidence": [file1.jpg, file2.mp4]
    }

    Returns: Updated evidence list
    """

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, report_id):
        """
        Add evidence to a report.
        """

        # Get the report
        report = get_object_or_404(Report, id=report_id)

        # Check if user is the reporter
        if report.reporter != request.user:
            return Response(
                {"error": "You can only add evidence to your own reports."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if report is still active
        if report.is_resolved:
            return Response(
                {"error": "Cannot add evidence to a resolved report."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the uploaded files
        files = request.FILES.getlist('evidence')

        if not files:
            return Response(
                {"error": "At least one file is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if adding would exceed max evidence count (5)
        current_count = report.evidence.count()
        if current_count + len(files) > 5:
            return Response(
                {"error": f"Maximum 5 evidence files allowed. You already have {current_count}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save each file as evidence
        new_evidence = []
        for file in files:
            evidence = self._save_evidence(report, file)
            new_evidence.append(evidence)

        # Return the updated evidence list
        serializer = ReportEvidenceSerializer(
            new_evidence,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _save_evidence(self, report, file):
        """
        Helper method to save a single evidence file.
        """

        # Determine evidence type from file extension
        ext = os.path.splitext(file.name)[1].lower()

        if ext in ['.jpg', '.jpeg', '.png']:
            evidence_type = ReportEvidence.EvidenceType.IMAGE
        elif ext in ['.mp4', '.mov']:
            evidence_type = ReportEvidence.EvidenceType.VIDEO
        elif ext in ['.mp3', '.wav']:
            evidence_type = ReportEvidence.EvidenceType.AUDIO
        else:
            raise serializers.ValidationError(f"Unsupported file type: {ext}")

        # Get MIME type
        mime_type = mimetypes.guess_type(file.name)[0] or ''

        # Create the evidence record
        return ReportEvidence.objects.create(
            report=report,
            file=file,
            evidence_type=evidence_type,
            original_filename=file.name,
            mime_type=mime_type,
            file_size=file.size
        )


# ============================================
# VIEW 7: CrowdVerificationView
# Handles crowd verification responses
# ============================================

class CrowdVerificationView(APIView):
    """
    API endpoint for citizens to respond to verification requests.

    WHO: Citizens (authenticated users)
    WHAT: Confirm or deny a report
    HOW: POST to /api/reports/{id}/verify/

    Flutter sends:
    {
        "response": "CONFIRM",
        "comment": "I see smoke from my window"
    }

    Returns: Verification status
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, report_id):
        """
        Submit a verification response.
        """

        # Get the report
        report = get_object_or_404(Report, id=report_id)

        # Check if report is in crowd verification stage
        if report.status != Report.Status.UNDER_CROWD_VERIFICATION:
            return Response(
                {"error": "This report is not under crowd verification."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user is the reporter (they can't verify their own report)
        if report.reporter == request.user:
            return Response(
                {"error": "You cannot verify your own report."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user is nearby
        # TODO: Implement distance check
        # if not self._is_user_nearby(request.user, report):
        #     return Response(
        #         {"error": "You must be nearby to verify this report."},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # Validate the data
        serializer = CrowdVerificationSerializer(
            data=request.data,
            context={'request': request}
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save the verification
        verification = serializer.save(report=report)

        # Update report crowd counts
        if verification.response == 'CONFIRM':
            report.crowd_confirmations += 1
        elif verification.response == 'DENY':
            report.crowd_denials += 1

        report.save()

        # Check if crowd verification threshold is met
        # If 3 confirmations, mark as verified
        if report.crowd_confirmations >= 3:
            report.status = Report.Status.VERIFIED
            report.is_verified = True
            report.verified_at = timezone.now()
            report.crowd_verification_completed = True
            report.save()

            # Award points
            report.award_points(50)

        # If 3 denials, mark as rejected
        elif report.crowd_denials >= 3:
            report.status = Report.Status.REJECTED
            report.crowd_verification_completed = True
            report.save()

        # Return the updated verification
        response_serializer = CrowdVerificationSerializer(
            verification,
            context={'request': request}
        )

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def get(self, request, report_id):
        """
        Get all verification responses for a report.
        """

        # Get the report
        report = get_object_or_404(Report, id=report_id)

        # Get all verification responses for this report
        verifications = CrowdVerification.objects.filter(report=report)

        serializer = CrowdVerificationSerializer(
            verifications,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)


# ============================================
# VIEW 8: DeleteReportView
# Allows citizens to delete their own reports
# ============================================

class DeleteReportView(generics.DestroyAPIView):
    """
    API endpoint to delete a report (soft delete).

    WHO: The reporter (citizen who created the report)
    WHAT: Soft delete (mark as inactive)
    HOW: DELETE to /api/reports/{id}/delete/

    Returns: Success message
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, report_id):
        """
        Delete a report (soft delete).
        """

        # Get the report
        report = get_object_or_404(Report, id=report_id)

        # Check if user is the reporter
        if report.reporter != request.user:
            return Response(
                {"error": "You can only delete your own reports."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if report is already resolved
        if report.is_resolved:
            return Response(
                {"error": "Cannot delete a resolved report."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Soft delete (mark as inactive)
        report.is_active = False
        report.save()

        return Response(
            {"message": "Report deleted successfully."},
            status=status.HTTP_200_OK
        )


# ============================================
# VIEW 9: ReportStatsView
# Get statistics about reports (Authorities only)
# ============================================

class ReportStatsView(APIView):
    """
    API endpoint for authorities to get report statistics.

    WHO: Authorities and Admins
    WHAT: Statistics about reports
    HOW: GET to /api/reports/stats/

    Returns: Report statistics
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get report statistics.
        """

        # Check if user is authority or admin
        if not (request.user.is_authority or request.user.is_admin):
            return Response(
                {"error": "Only authorities can view statistics."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get total counts
        total_reports = Report.objects.count()
        active_reports = Report.objects.filter(is_active=True).count()
        pending_reports = Report.objects.filter(
            status__in=[
                Report.Status.PENDING_AI_ANALYSIS,
                Report.Status.UNDER_CROWD_VERIFICATION,
                Report.Status.FLAGGED_FOR_REVIEW
            ]
        ).count()
        verified_reports = Report.objects.filter(is_verified=True).count()
        resolved_reports = Report.objects.filter(status=Report.Status.RESOLVED).count()

        # Get reports by type
        reports_by_type = {}
        for danger_type in Report.DangerType.choices:
            type_key = danger_type[0]
            count = Report.objects.filter(danger_type=type_key).count()
            if count > 0:
                reports_by_type[type_key] = count

        # Get reports by zone (using address)
        reports_by_zone = {}
        zones = ['Douala', 'Yaoundé', 'Bafoussam', 'Garoua', 'Maroua']
        for zone in zones:
            count = Report.objects.filter(address__icontains=zone).count()
            if count > 0:
                reports_by_zone[zone] = count

        # Calculate average severity
        avg_severity = Report.objects.filter(
            severity__isnull=False
        ).aggregate(avg=models.Avg('severity'))['avg'] or 0

        # Get daily reports (last 7 days)
        from datetime import timedelta
        daily_reports = []
        for i in range(7):
            date = timezone.now().date() - timedelta(days=i)
            count = Report.objects.filter(
                created_at__date=date
            ).count()
            daily_reports.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })

        return Response({
            'total_reports': total_reports,
            'active_reports': active_reports,
            'pending_reports': pending_reports,
            'verified_reports': verified_reports,
            'resolved_reports': resolved_reports,
            'average_severity': round(avg_severity, 1),
            'reports_by_type': reports_by_type,
            'reports_by_zone': reports_by_zone,
            'daily_reports': daily_reports,
        })