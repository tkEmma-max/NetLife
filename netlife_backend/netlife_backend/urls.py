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
    path('admin/', admin.site.urls),

    # 👇 COMMENTE OU SUPPRIME CES LIGNES
    # path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('api/schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('api/accounts/', include('accounts.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/ai/', include('ai_engine.urls')),
    path('api/alerts/', include('alerts.urls')),
    path('api/interventions/', include('interventions.urls')),
    path('api/notifications/', include('notifications.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)