from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import User
from .serializers import (
    UserRegistrationSerializer, UserProfileSerializer,
    UserUpdateSerializer, ChangePasswordSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    User Registration API Endpoint

    Flutter sends: POST /api/accounts/register/
    {
        "email": "marie@gmail.com",
        "username": "marie123",
        "password": "SecurePass123",
        "confirm_password": "SecurePass123",
        "phone_number": "+237650123456",
        "role": "CITIZEN"
    }

    Returns:
    {
        "user": { user data },
        "refresh": "JWT refresh token",
        "access": "JWT access token"
    }
    """

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)  # Anyone can register
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        # Validate and create user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserProfileSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    User Login API Endpoint

    Flutter sends: POST /api/accounts/login/
    {
        "email": "marie@gmail.com",
        "password": "SecurePass123"
    }

    Returns:
    {
        "user": { user data },
        "refresh": "JWT refresh token",
        "access": "JWT access token"
    }
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate input
        if not email or not password:
            return Response({
                'error': 'Please provide both email and password'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate using email (our custom authentication)
        user = authenticate(request, username=email, password=password)

        # If email auth fails, try username (backward compatibility)
        if user is None:
            user = authenticate(request, username=email, password=password)

        if user:
            # Check if user is active
            if not user.is_active:
                return Response({
                    'error': 'Your account has been deactivated'
                }, status=status.HTTP_403_FORBIDDEN)

            # Generate tokens
            refresh = RefreshToken.for_user(user)

            # Update last active timestamp
            user.last_active = timezone.now()
            user.save()

            return Response({
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({
                'error': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and Update User Profile

    Flutter sends (GET): /api/accounts/profile/
    Returns: User data

    Flutter sends (PATCH): /api/accounts/profile/
    {
        "username": "new_name",
        "phone_number": "+237678901234"
    }
    Returns: Updated user data
    """

    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)  # Must be logged in

    def get_object(self):
        """Get the current logged-in user"""
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        """Get profile - returns full user data"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    """
    Change User Password

    Flutter sends: POST /api/accounts/change-password/
    {
        "old_password": "OldPass123",
        "new_password": "NewSecurePass123",
        "confirm_new_password": "NewSecurePass123"
    }
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Check old password
        if not user.check_password(serializer.data.get('old_password')):
            return Response({
                'old_password': 'Wrong password.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(serializer.data.get('new_password'))
        user.save()

        return Response({
            'message': 'Password updated successfully'
        }, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    """
    List all users (Admin only)

    Flutter sends: GET /api/accounts/users/?role=CITIZEN
    Returns: List of users
    """

    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAdminUser,)  # Only admins can see all users

    def get_queryset(self):
        """Filter users by role if provided"""
        queryset = User.objects.all()
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        return queryset


class PointsView(APIView):
    """
    View and Manage User Points

    Flutter sends (GET): /api/accounts/points/
    Returns: Points information

    Flutter sends (POST): /api/accounts/points/redeem/
    {
        "points_to_redeem": 100
    }
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Get current points information"""
        user = request.user
        return Response({
            'total_points': user.total_points,
            'points_balance': user.points_balance,
            'money_earned_cfa': user.money_earned_cfa,
            'reports_submitted': user.total_reports_submitted
        })

    def post(self, request):
        """Redeem points for money"""
        user = request.user
        points_to_redeem = request.data.get('points_to_redeem', 0)

        if points_to_redeem <= 0:
            return Response({
                'error': 'Must redeem at least 1 point'
            }, status=status.HTTP_400_BAD_REQUEST)

        money_earned = user.redeem_points(points_to_redeem)

        if money_earned == 0:
            return Response({
                'error': 'Insufficient points balance'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': f'Successfully redeemed {points_to_redeem} points for {money_earned} CFA',
            'new_balance': user.points_balance,
            'total_earned_cfa': user.money_earned_cfa
        })