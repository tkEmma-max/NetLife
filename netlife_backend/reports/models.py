from django.db import models

# Create your models here.
# reports/models.py
# ============================================
# EXPLANATION: This file defines what data we store in the database
# Think of it as the blueprint for our database tables
# Each class = one table
# Each attribute = one column
# ============================================

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator


# ============================================
# MODEL 1: Report
# This is the MAIN table for citizen reports
# ============================================

class Report(models.Model):
    """
    The main Report model - stores EVERYTHING about a citizen's report

    Purpose: To track each danger report from submission to resolution
    Who uses it: Citizens submit, Authorities view, AI analyzes
    Where it fits: Core data model for the entire platform
    """

    # ---------- STATUS CHOICES ----------
    # These are the possible states a report can be in
    class Status(models.TextChoices):
        PENDING_AI_ANALYSIS = 'PENDING_AI', 'Pending AI Analysis'
        UNDER_CROWD_VERIFICATION = 'CROWD_VERIFY', 'Under Crowd Verification'
        VERIFIED = 'VERIFIED', 'Verified'
        REJECTED = 'REJECTED', 'Rejected'
        FLAGGED_FOR_REVIEW = 'FLAGGED', 'Flagged for Review'
        ALERT_CREATED = 'ALERT_CREATED', 'Alert Created'
        RESOLVED = 'RESOLVED', 'Resolved'

    # ---------- DANGER TYPE CHOICES ----------
    class DangerType(models.TextChoices):
        FIRE = 'FIRE', 'Fire'
        FLOOD = 'FLOOD', 'Flood'
        WASTE = 'WASTE', 'Illegal Waste'
        DEFORESTATION = 'DEFORESTATION', 'Deforestation'
        POLLUTION = 'POLLUTION', 'Pollution'
        ROAD_HAZARD = 'ROAD_HAZARD', 'Road Hazard'
        OTHER = 'OTHER', 'Other'

    # ============================================
    # USER RELATIONSHIP
    # ============================================

    # ForeignKey means "Each report belongs to ONE user"
    # on_delete=models.CASCADE means "If user is deleted, delete their reports"
    # related_name='reports' allows: user.reports.all() to get all reports
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        help_text="The citizen who submitted this report"
    )

    # ============================================
    # REPORT CONTENT
    # ============================================

    # Title - short description (max 200 characters)
    title = models.CharField(
        max_length=200,
        help_text="Short title of the danger (e.g., 'Fire at Mokolo Market')"
    )

    # Description - detailed explanation (unlimited text)
    description = models.TextField(
        help_text="Detailed description of what was observed"
    )

    # ============================================
    # DANGER CLASSIFICATION
    # ============================================

    # The type of danger (fire, flood, etc.)
    # Initially null, set by AI analysis
    danger_type = models.CharField(
        max_length=20,
        choices=DangerType.choices,
        null=True,
        blank=True,
        help_text="AI-detected or manually selected danger type"
    )

    # Severity level (1-10 scale)
    # 1-3: Low, 4-6: Medium, 7-8: High, 9-10: Critical
    severity = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Severity level (1-10, where 10 is most severe)"
    )

    # Confidence percentage (0-100)
    # How sure is the AI/crowd that this is real?
    confidence_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="AI confidence score (0-100%)"
    )

    # ============================================
    # LOCATION (GPS Data)
    # ============================================

    # DecimalField stores precise GPS coordinates
    # max_digits=10 means 10 total digits
    # decimal_places=7 means 7 digits after decimal (very precise!)
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        help_text="GPS Latitude of the danger location"
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        help_text="GPS Longitude of the danger location"
    )

    # Human-readable address (reverse geocoded from GPS)
    address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Human-readable address of the location"
    )

    # GPS accuracy (in meters)
    gps_accuracy = models.FloatField(
        null=True,
        blank=True,
        help_text="GPS accuracy in meters"
    )

    # ============================================
    # STATUS & TIMESTAMPS
    # ============================================

    # Current status of the report (see Status choices above)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING_AI_ANALYSIS,
        help_text="Current status of the report"
    )

    # When was this report created? (auto-set on creation)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the report was submitted"
    )

    # When was this report last updated? (auto-updated on save)
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the report was last updated"
    )

    # If report was verified by authorities, when?
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the report was verified"
    )

    # If report was resolved, when?
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the incident was resolved"
    )

    # ============================================
    # VERIFICATION & AUDIT
    # ============================================

    # Was this report verified by authorities?
    is_verified = models.BooleanField(
        default=False,
        help_text="Has an authority verified this report?"
    )

    # Who verified this report?
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_reports',
        help_text="Authority who verified this report"
    )

    # Is this report active? (false means archived/deleted)
    is_active = models.BooleanField(
        default=True,
        help_text="Is this report still active/visible?"
    )

    # ============================================
    # CROWD VERIFICATION DATA
    # ============================================

    # How many nearby citizens confirmed this report?
    crowd_confirmations = models.IntegerField(
        default=0,
        help_text="Number of nearby citizens who confirmed this report"
    )

    # How many nearby citizens denied this report?
    crowd_denials = models.IntegerField(
        default=0,
        help_text="Number of nearby citizens who denied this report"
    )

    # Has crowd verification been completed?
    crowd_verification_completed = models.BooleanField(
        default=False,
        help_text="Has crowd verification finished?"
    )

    # ============================================
    # POINTS (Reward System)
    # ============================================

    # Points awarded for this report
    points_awarded = models.IntegerField(
        default=0,
        help_text="Points awarded to the reporter"
    )

    # Money earned (CFA) for this report
    money_earned_cfa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Money earned in CFA for this report"
    )

    # ============================================
    # META DATA
    # ============================================

    # Device info (optional - for debugging)
    device_model = models.CharField(
        max_length=100,
        blank=True,
        help_text="Mobile device model used to submit"
    )

    # App version (optional - for debugging)
    app_version = models.CharField(
        max_length=20,
        blank=True,
        help_text="App version used to submit"
    )

    # ============================================
    # META CLASS - Database settings
    # ============================================

    class Meta:
        # Table name in database
        db_table = 'reports'

        # Indexes for faster queries
        indexes = [
            models.Index(fields=['reporter']),  # Find reports by user
            models.Index(fields=['status']),  # Find reports by status
            models.Index(fields=['danger_type']),  # Find reports by type
            models.Index(fields=['latitude', 'longitude']),  # Find reports by location
            models.Index(fields=['created_at']),  # Sort by date
            models.Index(fields=['-created_at']),  # Sort by newest first
            models.Index(fields=['is_verified']),  # Find verified reports
        ]

        # Default ordering (newest first)
        ordering = ['-created_at']

    # ============================================
    # STRING REPRESENTATION
    # ============================================

    def __str__(self):
        """What shows in admin panel"""
        return f"{self.title} - {self.reporter.email} ({self.get_status_display()})"

    # ============================================
    # PROPERTIES (Helper methods)
    # ============================================

    @property
    def is_pending(self):
        """Is this report still pending analysis?"""
        return self.status in [
            self.Status.PENDING_AI_ANALYSIS,
            self.Status.UNDER_CROWD_VERIFICATION,
            self.Status.FLAGGED_FOR_REVIEW
        ]

    @property
    def is_resolved(self):
        """Has this report been resolved?"""
        return self.status == self.Status.RESOLVED

    @property
    def location_display(self):
        """Return human-readable location"""
        if self.address:
            return self.address
        return f"{self.latitude}, {self.longitude}"

    # ============================================
    # METHODS (Actions)
    # ============================================

    def mark_as_verified(self, verified_by_user):
        """
        Mark this report as verified by authority
        Purpose: To officially validate the report
        """
        self.status = self.Status.VERIFIED
        self.is_verified = True
        self.verified_by = verified_by_user
        self.verified_at = timezone.now()
        self.save()

        # Award points to reporter
        # We'll implement this later in services.py

    def mark_as_resolved(self):
        """
        Mark this report as resolved
        Purpose: To close the incident
        """
        self.status = self.Status.RESOLVED
        self.resolved_at = timezone.now()
        self.save()

    def award_points(self, points):
        """
        Award points to the reporter
        Purpose: Reward citizens for verified reports
        """
        self.points_awarded = points
        self.reporter.add_points(points, f"Report #{self.id} verified")
        self.save()

    def get_evidence_urls(self):
        """
        Get all evidence URLs for this report
        Purpose: For frontend to display evidence
        """
        return [evidence.file.url for evidence in self.evidence.all()]


# ============================================
# MODEL 2: ReportEvidence
# This stores all uploaded files for a report
# ============================================

class ReportEvidence(models.Model):
    """
    Stores all evidence (images, videos, audio) for a report

    Purpose: To manage multiple files per report
    Who uses it: Citizens upload, Authorities view, AI analyzes
    Where it fits: Child of Report model (each report can have many evidence files)
    """

    # ---------- EVIDENCE TYPE CHOICES ----------
    class EvidenceType(models.TextChoices):
        IMAGE = 'IMAGE', 'Image'
        VIDEO = 'VIDEO', 'Video'
        AUDIO = 'AUDIO', 'Audio'

    # ============================================
    # RELATIONSHIPS
    # ============================================

    # ForeignKey to Report (each evidence belongs to one report)
    # related_name='evidence' allows: report.evidence.all()
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='evidence',
        help_text="The report this evidence belongs to"
    )

    # ============================================
    # FILE DATA
    # ============================================

    # The actual file (uploaded to media/reports/)
    # upload_to='reports/' means files go to media/reports/
    file = models.FileField(
        upload_to='reports/%Y/%m/%d/',  # Organized by year/month/day
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'mp4', 'mov', 'mp3', 'wav']
            )
        ],
        help_text="Uploaded evidence file (image, video, or audio)"
    )

    # What type of file is this?
    evidence_type = models.CharField(
        max_length=10,
        choices=EvidenceType.choices,
        help_text="Type of evidence (image, video, or audio)"
    )

    # File size in bytes (for display/validation)
    file_size = models.IntegerField(
        default=0,
        help_text="File size in bytes"
    )

    # ============================================
    # METADATA
    # ============================================

    # Original filename (for display)
    original_filename = models.CharField(
        max_length=255,
        help_text="Original filename from user's device"
    )

    # MIME type (e.g., image/jpeg, video/mp4)
    mime_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="MIME type of the file"
    )

    # Order of evidence (for display order)
    order = models.IntegerField(
        default=0,
        help_text="Display order of evidence"
    )

    # When was this uploaded?
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this evidence was uploaded"
    )

    # ============================================
    # META CLASS
    # ============================================

    class Meta:
        db_table = 'report_evidence'
        ordering = ['order', 'uploaded_at']

    # ============================================
    # STRING REPRESENTATION
    # ============================================

    def __str__(self):
        return f"Evidence for Report #{self.report.id} - {self.original_filename}"

    # ============================================
    # PROPERTIES
    # ============================================

    @property
    def file_extension(self):
        """Get file extension (e.g., .jpg, .mp4)"""
        import os
        return os.path.splitext(self.original_filename)[1].lower()

    @property
    def file_url(self):
        """Get the URL to access this file"""
        return self.file.url if self.file else None

    @property
    def is_image(self):
        """Is this an image?"""
        return self.evidence_type == self.EvidenceType.IMAGE

    @property
    def is_video(self):
        """Is this a video?"""
        return self.evidence_type == self.EvidenceType.VIDEO

    @property
    def is_audio(self):
        """Is this an audio file?"""
        return self.evidence_type == self.EvidenceType.AUDIO


# ============================================
# MODEL 3: CrowdVerification
# This tracks community verification requests
# ============================================

class CrowdVerification(models.Model):
    """
    Tracks crowd verification requests for reports with low AI confidence

    Purpose: To get community input when AI is uncertain
    Who uses it: Citizens nearby are asked to confirm/deny
    Where it fits: Verification layer between AI and Alert
    """

    # ---------- RESPONSE CHOICES ----------
    class ResponseChoice(models.TextChoices):
        CONFIRM = 'CONFIRM', 'I confirm this danger exists'
        DENY = 'DENY', 'I don\'t see this danger'
        UNSURE = 'UNSURE', 'I\'m not sure'

    # ============================================
    # RELATIONSHIPS
    # ============================================

    # Which report is being verified?
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='crowd_verifications',
        help_text="The report being verified by the crowd"
    )

    # Which citizen is responding?
    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='verification_responses',
        help_text="The citizen responding to the verification request"
    )

    # ============================================
    # VERIFICATION DATA
    # ============================================

    # What did the citizen respond?
    response = models.CharField(
        max_length=10,
        choices=ResponseChoice.choices,
        help_text="Citizen's response (confirm, deny, or unsure)"
    )

    # Optional comment from the citizen
    comment = models.TextField(
        blank=True,
        help_text="Optional comment from the citizen"
    )

    # When did they respond?
    responded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the citizen responded"
    )

    # Was this response verified? (to prevent fake responses)
    is_verified = models.BooleanField(
        default=False,
        help_text="Is this response verified as genuine?"
    )

    # ============================================
    # META CLASS
    # ============================================

    class Meta:
        db_table = 'crowd_verifications'
        # Ensure one response per citizen per report
        unique_together = ['report', 'citizen']

    # ============================================
    # STRING REPRESENTATION
    # ============================================

    def __str__(self):
        return f"{self.citizen.email} - {self.response} - Report #{self.report.id}"