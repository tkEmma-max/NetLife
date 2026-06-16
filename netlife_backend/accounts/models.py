from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User Model for NetLife Platform

    This model extends Django's built-in User model with additional
    fields specific to our application.

    Why we extend AbstractUser:
    - Django already provides username, password, email, etc.
    - We add our own fields without rewriting everything
    """

    # Role choices for different user types
    class Role(models.TextChoices):
        CITIZEN = 'CITIZEN', 'Citizen'
        AUTHORITY = 'AUTHORITY', 'Authority'
        INTERVENTION_TEAM = 'INTERVENTION_TEAM', 'Intervention Team'
        ADMIN = 'ADMIN', 'Administrator'

    # Basic user information
    email = models.EmailField(unique=True, help_text="User's email address (used for login)")
    phone_number = models.CharField(max_length=20, blank=True, help_text="Phone number for SMS alerts")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CITIZEN)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    # Location fields for authorities and intervention teams
    assigned_zone = models.CharField(max_length=100, blank=True, help_text="Zone/Area this user is responsible for")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    # Verification and status
    is_verified = models.BooleanField(default=False, help_text="Has this user verified their email/phone?")
    verification_token = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True, help_text="Is this user account active?")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(default=timezone.now)

    # Statistics
    total_reports_submitted = models.IntegerField(default=0)
    total_interventions_completed = models.IntegerField(default=0)

    # Points System (Our hackathon winning feature!)
    total_points = models.IntegerField(default=0, help_text="Total points earned from verified reports")
    points_balance = models.IntegerField(default=0, help_text="Available points that can be redeemed")
    money_earned_cfa = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # User must use email for login, not username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['assigned_zone']),
            models.Index(fields=['is_verified']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        """String representation for admin panel"""
        return f"{self.email} ({self.get_role_display()})"

    @property
    def is_citizen(self):
        """Check if user is a citizen"""
        return self.role == self.Role.CITIZEN

    @property
    def is_authority(self):
        """Check if user is an authority"""
        return self.role == self.Role.AUTHORITY

    @property
    def is_intervention_team(self):
        """Check if user is on intervention team"""
        return self.role == self.Role.INTERVENTION_TEAM

    @property
    def is_admin(self):
        """Check if user is admin"""
        return self.role == self.Role.ADMIN

    def add_points(self, points, reason=""):
        """Add points to user and update balance"""
        self.total_points += points
        self.points_balance += points
        self.save()

        # Log this in a separate table (we'll create PointsHistory later)
        return f"Added {points} points. Reason: {reason}"

    def redeem_points(self, points_to_redeem):
        """Redeem points for money"""
        if self.points_balance >= points_to_redeem:
            self.points_balance -= points_to_redeem
            money_earned = points_to_redeem * 5  # 1 point = 5 CFA
            self.money_earned_cfa += money_earned
            self.save()
            return money_earned
        return 0