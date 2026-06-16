from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration

    This handles:
    1. Validating the data sent from Flutter
    2. Creating a new user
    3. Hashing the password
    """

    password = serializers.CharField(
        write_only=True,  # Never send password back to Flutter
        required=True,
        validators=[validate_password]  # Django's built-in password validation
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'confirm_password',
            'phone_number', 'role', 'assigned_zone'
        )
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        """
        Check that password and confirm_password match
        """
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        """
        Create a new user with hashed password
        """
        # Remove confirm_password (not needed for user creation)
        validated_data.pop('confirm_password')

        # Create user with hashed password
        user = User.objects.create_user(**validated_data)

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing user profile

    This is what gets sent to Flutter when viewing profile
    """

    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'phone_number', 'role', 'role_display',
            'profile_picture', 'assigned_zone', 'is_verified',
            'total_reports_submitted', 'total_interventions_completed',
            'total_points', 'points_balance', 'money_earned_cfa',
            'created_at', 'last_active'
        )
        read_only_fields = (
            'id', 'role', 'is_verified',
            'total_reports_submitted', 'total_interventions_completed',
            'total_points', 'points_balance', 'money_earned_cfa',
            'created_at', 'last_active'
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile
    """

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'profile_picture', 'assigned_zone')

    def update(self, instance, validated_data):
        """
        Update user fields
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Check that new passwords match
        """
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({
                "new_password": "Password fields didn't match."
            })
        return attrs