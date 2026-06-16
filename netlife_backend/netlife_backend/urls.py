# netlife_backend/urls.py
# ============================================
# EXPLANATION: Main URL configuration for the entire project
# This includes all apps: accounts, reports, ai_engine, etc.
# ============================================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Accounts app (authentication)
    path('api/accounts/', include('accounts.urls')),

    # ==========================================
    # REPORTS APP - ADD THIS LINE!
    # ==========================================
    # All report URLs will start with /api/reports/
    path('api/reports/', include('reports.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)