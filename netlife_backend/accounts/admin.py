from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for User model
    Makes it easier to manage users in Django admin
    """

    # What columns to show in the list view
    list_display = ('email', 'username', 'role', 'is_verified', 'is_active', 'total_points', 'created_at')

    # What filters to show on the right side
    list_filter = ('role', 'is_verified', 'is_active', 'created_at')

    # What fields to search
    search_fields = ('email', 'username', 'phone_number')

    # Default ordering
    ordering = ('-created_at',)

    # Add our custom fields to the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('NetLife Additional Info', {
            'fields': (
                'phone_number', 'role', 'profile_picture',
                'assigned_zone', 'latitude', 'longitude',
                'is_verified', 'verification_token',
                'total_reports_submitted', 'total_interventions_completed',
                'total_points', 'points_balance', 'money_earned_cfa'
            )
        }),
    )

    # What fields to show when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('NetLife Additional Info', {
            'fields': (
                'email', 'phone_number', 'role', 'assigned_zone'
            )
        }),
    )