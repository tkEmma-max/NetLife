# reports/serializers.py
# ============================================
# EXPLANATION: This file converts Python objects to JSON and back
# Each serializer corresponds to a model
# Purpose: To send/receive data from the Flutter app
# ============================================

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Report, ReportEvidence, CrowdVerification
from django.core.exceptions import ValidationError
import os

# Get the User model
User = get_user_model()


# ============================================
# SERIALIZER 1: ReportEvidenceSerializer
# Handles evidence files (images, videos, audio)
# ============================================

class ReportEvidenceSerializer(serializers.ModelSerializer):
    """
    Serializer for ReportEvidence model.
    Handles uploading and displaying evidence files.

    Purpose: To show evidence files in API responses
    Who uses it: Flutter app to display photos/videos
    """

    # We'll add a custom field to show the full URL of the file
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ReportEvidence
        fields = [
            'id',
            'file',  # The actual file (uploaded)
            'file_url',  # Full URL to access file
            'evidence_type',  # IMAGE, VIDEO, or AUDIO
            'original_filename',  # Original name from phone
            'mime_type',  # image/jpeg, video/mp4, etc.
            'file_size',  # Size in bytes
            'order',  # Display order
            'uploaded_at'  # When uploaded
        ]
        read_only_fields = [
            'id',
            'file_url',
            'mime_type',
            'file_size',
            'uploaded_at'
        ]

    def get_file_url(self, obj):
        """
        Get the full URL to access the file.

        Purpose: Flutter needs the full URL to download the image.
        Without this, Flutter only gets the path (media/reports/photo.jpg)
        """
        request = self.context.get('request')
        if request and obj.file:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None


# ============================================
# SERIALIZER 2: ReportSerializer
# Main serializer for Report model
# ============================================

class ReportSerializer(serializers.ModelSerializer):
    """
    Main serializer for Report model.
    Handles creating, viewing, and updating reports.

    Purpose: To send report data to Flutter and receive from Flutter
    Who uses it: Citizens submit reports, Authorities view reports
    """

    # ============================================
    # NESTED SERIALIZERS
    # ============================================

    # We include the evidence as a nested list
    # This means when someone views a report, they see ALL evidence
    evidence = ReportEvidenceSerializer(many=True, read_only=True)

    # We include reporter details (but hide sensitive info)
    reporter_email = serializers.EmailField(source='reporter.email', read_only=True)
    reporter_username = serializers.CharField(source='reporter.username', read_only=True)

    # Display the status as a readable string
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    danger_type_display = serializers.CharField(source='get_danger_type_display', read_only=True)

    # ============================================
    # META CLASS
    # ============================================

    class Meta:
        model = Report
        fields = [
            # Identification
            'id',

            # User who reported
            'reporter',
            'reporter_email',
            'reporter_username',

            # Content
            'title',
            'description',

            # Classification
            'danger_type',
            'danger_type_display',
            'severity',
            'confidence_score',

            # Location
            'latitude',
            'longitude',
            'address',
            'gps_accuracy',

            # Status
            'status',
            'status_display',
            'is_verified',
            'is_active',

            # Timestamps
            'created_at',
            'updated_at',
            'verified_at',
            'resolved_at',

            # Verification
            'verified_by',
            'crowd_confirmations',
            'crowd_denials',
            'crowd_verification_completed',

            # Reward
            'points_awarded',
            'money_earned_cfa',

            # Evidence
            'evidence',  # List of evidence files
        ]

        # Fields that CANNOT be modified by the user
        read_only_fields = [
            'id',
            'reporter',
            'reporter_email',
            'reporter_username',
            'status',
            'status_display',
            'danger_type_display',
            'is_verified',
            'created_at',
            'updated_at',
            'verified_at',
            'resolved_at',
            'verified_by',
            'crowd_confirmations',
            'crowd_denials',
            'crowd_verification_completed',
            'points_awarded',
            'money_earned_cfa',
            'evidence',
        ]

    # ============================================
    # CREATE METHOD - Called when Flutter submits a report
    # ============================================

    def create(self, validated_data):
        """
        Create a new report.

        Called when: Flutter POSTs to /api/reports/submit/
        What it does: Creates the report, sets the reporter, handles evidence

        Purpose: To save a new report from a citizen
        """

        # Get the current user from the request
        # The user is passed in the context when we call the serializer
        request = self.context.get('request')
        user = request.user if request else None

        # Set the reporter to the current user
        validated_data['reporter'] = user

        # For now, status starts as PENDING_AI_ANALYSIS
        # We'll change it after AI analysis
        validated_data['status'] = Report.Status.PENDING_AI_ANALYSIS

        # Create the report
        report = Report.objects.create(**validated_data)

        # The evidence will be handled separately (in the view)
        # We'll add evidence after the report is created

        return report

    # ============================================
    # UPDATE METHOD - Called when Flutter updates a report
    # ============================================

    def update(self, instance, validated_data):
        """
        Update an existing report.

        Called when: Flutter PATCHes /api/reports/{id}/
        What it does: Updates only the fields sent
        """

        # List of fields that can be updated by the reporter
        allowed_fields = ['title', 'description']

        for field in allowed_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance

    # ============================================
    # VALIDATION METHODS
    # ============================================

    def validate_title(self, value):
        """
        Validate the title field.

        Purpose: Ensure title isn't too short or too long
        """
        if len(value) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters long."
            )
        if len(value) > 200:
            raise serializers.ValidationError(
                "Title must be less than 200 characters."
            )
        return value

    def validate_description(self, value):
        """
        Validate the description field.

        Purpose: Ensure description isn't too short
        """
        if len(value) < 10:
            raise serializers.ValidationError(
                "Please provide more details in the description (at least 10 characters)."
            )
        return value

    def validate_latitude(self, value):
        """
        Validate latitude.

        Purpose: Ensure latitude is within valid range (-90 to 90)
        """
        if not (-90 <= float(value) <= 90):
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90 degrees."
            )
        return value

    def validate_longitude(self, value):
        """
        Validate longitude.

        Purpose: Ensure longitude is within valid range (-180 to 180)
        """
        if not (-180 <= float(value) <= 180):
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180 degrees."
            )
        return value


# ============================================
# SERIALIZER 3: ReportCreateSerializer
# Special serializer for creating reports with evidence
# ============================================

class ReportCreateSerializer(serializers.Serializer):
    """
    Special serializer for creating reports with files.

    Purpose: To handle report submission with evidence files
    Why separate: We need to handle file uploads separately from text

    Called by: Flutter when submitting a new report
    """

    # Text fields
    title = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(required=True)

    # Location fields
    latitude = serializers.DecimalField(max_digits=10, decimal_places=7, required=True)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=7, required=True)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    gps_accuracy = serializers.FloatField(required=False, allow_null=True)

    # File fields (these will be handled separately in the view)
    # We don't include them here because they're handled as files
    evidence = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        help_text="List of evidence files (max 3)"
    )

    # ============================================
    # VALIDATION
    # ============================================

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters.")
        return value

    def validate_evidence(self, value):
        """
        Validate evidence files.
        Purpose: Ensure max 3 files and correct types
        """
        if not value:
            raise serializers.ValidationError(
                "At least one piece of evidence is required."
            )

        if len(value) > 3:
            raise serializers.ValidationError(
                "Maximum 3 pieces of evidence allowed."
            )

        # Check file types
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov', '.mp3', '.wav']
        for file in value:
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in allowed_extensions:
                raise serializers.ValidationError(
                    f"Invalid file type: {ext}. Allowed: {', '.join(allowed_extensions)}"
                )

            # Check file size
            if file.size > 50 * 1024 * 1024:  # 50MB
                raise serializers.ValidationError(
                    f"File {file.name} is too large. Max size is 50MB."
                )

        return value


# ============================================
# SERIALIZER 4: CrowdVerificationSerializer
# Handles crowd verification responses
# ============================================

class CrowdVerificationSerializer(serializers.ModelSerializer):
    """
    Serializer for CrowdVerification model.

    Purpose: To handle crowd verification requests and responses
    Who uses it: Citizens confirming/denying reports

    Called when: Flutter sends a verification response
    """

    # Display citizen info (but hide sensitive data)
    citizen_email = serializers.EmailField(source='citizen.email', read_only=True)
    citizen_username = serializers.CharField(source='citizen.username', read_only=True)

    # Display response as readable string
    response_display = serializers.CharField(source='get_response_display', read_only=True)

    class Meta:
        model = CrowdVerification
        fields = [
            'id',
            'report',
            'citizen',
            'citizen_email',
            'citizen_username',
            'response',
            'response_display',
            'comment',
            'responded_at',
            'is_verified'
        ]
        read_only_fields = [
            'id',
            'citizen',
            'citizen_email',
            'citizen_username',
            'responded_at',
            'is_verified'
        ]

    def create(self, validated_data):
        """
        Create a crowd verification response.

        Called when: A citizen responds to a verification request
        Purpose: To record citizen's confirmation/denial
        """
        # Get the current user
        request = self.context.get('request')
        user = request.user if request else None

        # Set the citizen to the current user
        validated_data['citizen'] = user

        # Check if citizen already responded to this report
        existing = CrowdVerification.objects.filter(
            report=validated_data['report'],
            citizen=user
        ).first()

        if existing:
            # Update existing response
            existing.response = validated_data['response']
            existing.comment = validated_data.get('comment', '')
            existing.save()
            return existing

        # Create new response
        return super().create(validated_data)


# ============================================
# SERIALIZER 5: ReportStatusUpdateSerializer
# For authorities to update report status
# ============================================

class ReportStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating report status (Authorities only).

    Purpose: To allow authorities to verify, reject, or flag reports
    Who uses it: Authority users
    """

    status = serializers.ChoiceField(
        choices=[
            'VERIFIED',
            'REJECTED',
            'FLAGGED',
            'ALERT_CREATED',
            'RESOLVED'
        ],
        required=True,
        help_text="New status for the report"
    )

    comment = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional comment explaining the status change"
    )

    def validate(self, data):
        """
        Validate the status update.
        Purpose: Ensure status changes are valid
        """
        report = self.context.get('report')

        # Check if report is already resolved
        if report and report.status == 'RESOLVED':
            raise serializers.ValidationError(
                "Cannot change status of a resolved report."
            )

        return data


# ============================================
# SERIALIZER 6: ReportNearbySerializer
# For showing nearby reports (limited data)
# ============================================

class ReportNearbySerializer(serializers.ModelSerializer):
    """
    Simplified serializer for nearby reports.

    Purpose: To show only essential info for nearby alerts
    Why limited: Saves bandwidth, faster response
    """

    distance_km = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    danger_type_display = serializers.CharField(source='get_danger_type_display', read_only=True)

    class Meta:
        model = Report
        fields = [
            'id',
            'title',
            'danger_type',
            'danger_type_display',
            'severity',
            'status',
            'status_display',
            'latitude',
            'longitude',
            'address',
            'created_at',
            'distance_km'
        ]

    def get_distance_km(self, obj):
        """
        Calculate distance from user's location.
        Purpose: To show "2.5 km away"
        """
        request = self.context.get('request')
        if not request:
            return None

        # Get user's location from query params
        user_lat = request.query_params.get('latitude')
        user_lng = request.query_params.get('longitude')

        if user_lat and user_lng:
            from math import radians, sin, cos, sqrt, atan2

            # Convert to radians
            lat1 = radians(float(user_lat))
            lon1 = radians(float(user_lng))
            lat2 = radians(float(obj.latitude))
            lon2 = radians(float(obj.longitude))

            # Haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = 6371 * c  # Earth's radius in km

            return round(distance, 2)

        return None