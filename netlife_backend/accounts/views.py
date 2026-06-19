# accounts/views.py
# ============================================
# AJOUTER CETTE CLASSE AU DÉBUT DU FICHIER
# ============================================

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer
)
from django.utils import timezone  # ⬅️ AJOUTER CETTE LIGNE


# ============================================
# CLASSE 1: RegisterView (INSCRIPTION)
# ============================================

class RegisterView(generics.CreateAPIView):
    """
    Vue d'inscription pour les nouveaux utilisateurs.

    Supporte à la fois JSON et formulaire HTML.

    UTILISATION AVEC FORMULAIRE (Navigateur):
        GET /api/accounts/register/ → Affiche le formulaire
        POST /api/accounts/register/ → Soumet le formulaire

    UTILISATION AVEC JSON (API/Flutter):
        POST /api/accounts/register/
        {
            "email": "user@example.com",
            "username": "user123",
            "password": "monpassword",
            "confirm_password": "monpassword",
            "phone_number": "+237650123456",
            "role": "CITIZEN"
        }
    """

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def get(self, request):
        """
        Affiche le formulaire d'inscription pour le navigateur.
        """
        return render(request, 'accounts/register.html', {
            'title': 'Inscription - NetLife'
        })

    def post(self, request, *args, **kwargs):
        """
        Gère l'inscription via formulaire OU JSON.
        """

        # ============================================
        # CAS 1: Soumission depuis le formulaire HTML
        # ============================================
        if request.content_type == 'application/x-www-form-urlencoded':
            # Récupérer les données du formulaire
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            phone_number = request.POST.get('phone_number', '')
            role = request.POST.get('role', 'CITIZEN')

            # Valider les champs
            errors = {}

            if not email:
                errors['email'] = 'L\'email est requis'
            elif User.objects.filter(email=email).exists():
                errors['email'] = 'Cet email est déjà utilisé'

            if not username:
                errors['username'] = 'Le nom d\'utilisateur est requis'
            elif User.objects.filter(username=username).exists():
                errors['username'] = 'Ce nom d\'utilisateur est déjà utilisé'

            if not password:
                errors['password'] = 'Le mot de passe est requis'
            elif len(password) < 8:
                errors['password'] = 'Le mot de passe doit contenir au moins 8 caractères'
            elif password != confirm_password:
                errors['confirm_password'] = 'Les mots de passe ne correspondent pas'

            if errors:
                return render(request, 'accounts/register.html', {
                    'errors': errors,
                    'form_data': request.POST
                })

            # Créer l'utilisateur
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone_number=phone_number,
                role=role
            )

            # Connecter l'utilisateur automatiquement
            auth_login(request, user)

            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)

            # Rediriger vers la page de succès
            return render(request, 'accounts/register_success.html', {
                'user': user,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })

        # ============================================
        # CAS 2: Requête JSON (Flutter / API)
        # ============================================
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)


# ============================================
# CLASSE 2: LoginView (CONNEXION)
# ============================================

class LoginView(APIView):
    """
    Vue de login supportant à la fois JSON et formulaire HTML.

    UTILISATION AVEC FORMULAIRE (Navigateur):
        GET /api/accounts/login/ → Affiche le formulaire
        POST /api/accounts/login/ → Soumet le formulaire

    UTILISATION AVEC JSON (API/Flutter):
        POST /api/accounts/login/
        {
            "email": "user@example.com",
            "password": "monpassword"
        }
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """
        Affiche le formulaire de login pour le navigateur.
        """
        return render(request, 'accounts/login.html', {
            'title': 'Connexion - NetLife'
        })

    def post(self, request):
        """
        Gère la soumission du formulaire OU du JSON.
        """

        # ============================================
        # CAS 1: Soumission depuis le formulaire HTML
        # ============================================
        if request.content_type == 'application/x-www-form-urlencoded':
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Valider les champs
            if not email or not password:
                return render(request, 'accounts/login.html', {
                    'error': 'Veuillez remplir tous les champs'
                })

            # Authentifier l'utilisateur
            user = authenticate(request, username=email, password=password)

            if user is None:
                return render(request, 'accounts/login.html', {
                    'error': 'Email ou mot de passe incorrect'
                })

            # Vérifier si le compte est actif
            if not user.is_active:
                return render(request, 'accounts/login.html', {
                    'error': 'Votre compte a été désactivé'
                })

            # Connecter l'utilisateur
            auth_login(request, user)

            # Mettre à jour la dernière connexion
            user.last_active = timezone.now()
            user.save()

            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)

            # Afficher la page de succès
            return render(request, 'accounts/login_success.html', {
                'user': user,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })

        # ============================================
        # CAS 2: Requête JSON (Flutter / API)
        # ============================================
        else:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({
                    'error': 'Veuillez fournir email et mot de passe'
                }, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, username=email, password=password)

            if user is None:
                return Response({
                    'error': 'Email ou mot de passe incorrect'
                }, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
                return Response({
                    'error': 'Votre compte a été désactivé'
                }, status=status.HTTP_403_FORBIDDEN)

            user.last_active = timezone.now()
            user.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })


# ============================================
# CLASSE 3: ProfileView (PROFIL)
# ============================================

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Vue pour voir et modifier le profil.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


# ============================================
# CLASSE 4: ChangePasswordView (CHANGER MOT DE PASSE)
# ============================================

class ChangePasswordView(APIView):
    """
    Vue pour changer le mot de passe.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.data.get('old_password')):
            return Response({
                'old_password': 'Mot de passe incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.data.get('new_password'))
        user.save()

        return Response({
            'message': 'Mot de passe mis à jour avec succès'
        }, status=status.HTTP_200_OK)


# ============================================
# CLASSE 5: UserListView (LISTE DES UTILISATEURS - Admin)
# ============================================

class UserListView(generics.ListAPIView):
    """
    Vue pour lister les utilisateurs (Admin uniquement).
    """
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        return queryset


# ============================================
# CLASSE 6: PointsView (POINTS - Nouveau)
# ============================================

class PointsView(APIView):
    """
    Vue pour voir et gérer les points.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response({
            'total_points': user.total_points,
            'points_balance': user.points_balance,
            'money_earned_cfa': user.money_earned_cfa,
            'reports_submitted': user.total_reports_submitted
        })

    def post(self, request):
        user = request.user
        points_to_redeem = request.data.get('points_to_redeem', 0)

        if points_to_redeem <= 0:
            return Response({
                'error': 'Vous devez échanger au moins 1 point'
            }, status=status.HTTP_400_BAD_REQUEST)

        money_earned = user.redeem_points(points_to_redeem)

        if money_earned == 0:
            return Response({
                'error': 'Solde de points insuffisant'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': f'Vous avez échangé {points_to_redeem} points pour {money_earned} CFA',
            'new_balance': user.points_balance,
            'total_earned_cfa': user.money_earned_cfa
        })