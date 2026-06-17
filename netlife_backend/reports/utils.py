# reports/utils.py
# ============================================
# COMPLETE FILE - INCLUDES ALL FUNCTIONS
# ============================================

import os
import mimetypes
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta


# ============================================
# FILE VALIDATION FUNCTIONS
# ============================================

def validate_file_extension(filename):
    """Validate that the file has an allowed extension."""
    allowed_extensions = {
        '.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp',
        '.mp4', '.mov', '.avi', '.mkv', '.webm',
        '.mp3', '.wav', '.m4a', '.aac', '.ogg'
    }

    ext = os.path.splitext(filename)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError(
            f"File type '{ext}' is not allowed. "
            f"Allowed types: {', '.join(sorted(allowed_extensions))}"
        )

    return True


def validate_file_size(file, max_size_mb=50):
    """Validate that the file is not too large."""
    max_size_bytes = max_size_mb * 1024 * 1024

    if file.size > max_size_bytes:
        raise ValidationError(
            f"File is too large. Maximum size is {max_size_mb}MB. "
            f"Your file is {file.size / (1024 * 1024):.1f}MB."
        )

    return True


def validate_evidence_count(current_count, new_count, max_evidence=5):
    """Validate that total evidence count doesn't exceed maximum."""
    if current_count + new_count > max_evidence:
        raise ValidationError(
            f"Cannot add {new_count} files. "
            f"You already have {current_count} files. "
            f"Maximum is {max_evidence} files per report."
        )

    return True


# ============================================
# EVIDENCE TYPE DETECTION
# ============================================

def get_evidence_type_from_filename(filename):
    """Determine the evidence type from the filename extension."""
    ext = os.path.splitext(filename)[1].lower()

    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
        return 'IMAGE'
    elif ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
        return 'VIDEO'
    elif ext in ['.mp3', '.wav', '.m4a', '.aac', '.ogg']:
        return 'AUDIO'
    else:
        return None


def get_mime_type(filename):
    """Get the MIME type of a file."""
    mime_type = mimetypes.guess_type(filename)[0]
    return mime_type or 'application/octet-stream'


def generate_unique_filename(original_filename, report_id):
    """Generate a unique filename for uploaded files."""
    ext = os.path.splitext(original_filename)[1].lower()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_name = f"{report_id}_{timestamp}_{os.path.basename(original_filename)}"
    return unique_name


# ============================================
# GPS AND LOCATION UTILITIES
# ============================================

def is_coordinate_in_cameroon(latitude, longitude):
    """Check if GPS coordinates are within Cameroon."""
    LAT_MIN, LAT_MAX = 2.0, 13.0
    LON_MIN, LON_MAX = 8.0, 16.0

    try:
        lat = float(latitude)
        lng = float(longitude)
    except (TypeError, ValueError):
        return False

    return LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lng <= LON_MAX


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates in kilometers."""
    from math import radians, sin, cos, sqrt, atan2

    lat1_rad = radians(float(lat1))
    lon1_rad = radians(float(lon1))
    lat2_rad = radians(float(lat2))
    lon2_rad = radians(float(lon2))

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    R = 6371
    distance = R * c

    return round(distance, 2)


def get_location_display(latitude, longitude, address=""):
    """Get a human-readable location display."""
    if address:
        return f"{address} ({latitude}, {longitude})"
    return f"{latitude}, {longitude}"


# ============================================
# REPORT STATUS HELPERS
# ============================================

def get_status_display(status_code):
    """Get the human-readable display for a status code."""
    status_map = {
        'PENDING_AI': 'Pending AI Analysis',
        'CROWD_VERIFY': 'Under Crowd Verification',
        'VERIFIED': 'Verified',
        'REJECTED': 'Rejected',
        'FLAGGED': 'Flagged for Review',
        'ALERT_CREATED': 'Alert Created',
        'RESOLVED': 'Resolved'
    }
    return status_map.get(status_code, status_code)


def is_urgent_report(report):
    """Check if a report is urgent (needs immediate attention)."""
    urgent_statuses = ['PENDING_AI', 'CROWD_VERIFY', 'FLAGGED']

    if report.status in urgent_statuses and report.severity and report.severity >= 7:
        return True

    one_hour_ago = timezone.now() - timedelta(hours=1)
    if report.created_at >= one_hour_ago:
        if report.status in urgent_statuses:
            return True

    return False


def get_priority_level(report):
    """Get the priority level of a report."""
    if not report.severity:
        return 'LOW'

    if report.severity >= 8:
        return 'HIGH'
    elif report.severity >= 5:
        return 'MEDIUM'
    else:
        return 'LOW'


# ============================================
# CROWD VERIFICATION HELPERS
# ============================================

def calculate_crowd_confidence(confirmations, denials):
    """Calculate confidence based on crowd verification responses."""
    total = confirmations + denials

    if total == 0:
        return 0

    confidence = (confirmations / total) * 100
    return round(confidence, 2)


def is_crowd_verification_complete(confirmations, denials, threshold=3):
    """Check if crowd verification is complete."""
    return confirmations >= threshold or denials >= threshold


# ============================================
# POINTS CALCULATION HELPERS
# ============================================

def calculate_points_for_report(severity, confidence, is_first_reporter=False):
    """Calculate points to award for a report."""
    if severity >= 8:
        base_points = 100
    elif severity >= 5:
        base_points = 50
    elif severity >= 3:
        base_points = 25
    else:
        base_points = 10

    if confidence >= 90:
        confidence_bonus = 50
    elif confidence >= 70:
        confidence_bonus = 25
    else:
        confidence_bonus = 0

    first_reporter_bonus = 50 if is_first_reporter else 0

    return base_points + confidence_bonus + first_reporter_bonus


def calculate_money_for_points(points):
    """Calculate money (CFA) from points."""
    EXCHANGE_RATE = 5
    return points * EXCHANGE_RATE


# ============================================
# DANGER TYPE HELPERS
# ============================================

def get_danger_type_emoji(danger_type):
    """Get an emoji for a danger type."""
    emoji_map = {
        'FIRE': '🔥',
        'FLOOD': '🌊',
        'WASTE': '🗑️',
        'DEFORESTATION': '🌳',
        'POLLUTION': '☠️',
        'ROAD_HAZARD': '🚧',
        'OTHER': '⚠️'
    }
    return emoji_map.get(danger_type, '⚠️')


def get_danger_type_color(danger_type):
    """Get a color for a danger type."""
    color_map = {
        'FIRE': '#FF0000',
        'FLOOD': '#0066FF',
        'WASTE': '#8B4513',
        'DEFORESTATION': '#008000',
        'POLLUTION': '#800080',
        'ROAD_HAZARD': '#FFA500',
        'OTHER': '#808080'
    }
    return color_map.get(danger_type, '#808080')


# ============================================
# STRING UTILITIES
# ============================================

def truncate_text(text, max_length=100, suffix="..."):
    """Truncate text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + suffix


def clean_text(text):
    """Clean text by removing extra spaces and special characters."""
    import re
    text = ' '.join(text.split())
    text = re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', text)
    return text


# ============================================
# ⭐ NEW FUNCTION - EVIDENCE UPLOAD HANDLER
# ============================================

def handle_evidence_upload(report, files):
    """
    Handle uploading multiple evidence files for a report.

    Purpose: To process and save evidence files from a request
    Usage: Called from views when submitting reports

    Parameters:
        report: The Report instance to attach evidence to
        files: List of uploaded file objects

    Returns: List of created Evidence objects

    Example:
        evidence_list = handle_evidence_upload(report, request.FILES.getlist('evidence'))
    """
    from .models import ReportEvidence

    created_evidence = []

    if not files:
        return created_evidence

    # Limit to 3 files
    if len(files) > 3:
        raise ValidationError("Maximum 3 evidence files allowed.")

    for file in files:
        # Validate the file
        validate_file_extension(file.name)
        validate_file_size(file)

        # Determine evidence type
        evidence_type = get_evidence_type_from_filename(file.name)
        if not evidence_type:
            raise ValidationError(f"Unsupported file type: {file.name}")

        # Get MIME type
        mime_type = get_mime_type(file.name)

        # Create the evidence record
        evidence = ReportEvidence.objects.create(
            report=report,
            file=file,
            evidence_type=evidence_type,
            original_filename=file.name,
            mime_type=mime_type,
            file_size=file.size,
            order=len(created_evidence)  # Maintain order
        )

        created_evidence.append(evidence)

    return created_evidence