# reports/apps.py
# ============================================
# EXPLANATION: App Configuration
# This registers the app with Django
# ============================================

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """
    Configuration for the Reports app.

    Purpose: To configure the app for Django
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
    verbose_name = 'Reports Management'

    def ready(self):
        """
        Called when Django starts.

        Purpose: To import signals (if any)
        """
        # Import signals here later if needed
        pass