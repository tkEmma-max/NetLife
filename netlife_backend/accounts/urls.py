from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),

    # Admin endpoints
    path('users/', views.UserListView.as_view(), name='user-list'),

    # Points endpoints
    path('points/', views.PointsView.as_view(), name='points'),
]