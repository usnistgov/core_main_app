""" Apps file for setting core package when app is ready.
"""
import sys

from django.apps import AppConfig
from django.conf import settings


class InitApp(AppConfig):
    """Core application settings."""

    verbose_name = "Core Main App"

    name = "core_main_app"
    """ :py:class:`str`: Package name
    """

    def ready(self):
        from core_main_app.permissions import discover
        from core_main_app.settings import SSL_CERTIFICATES_DIR
        from core_main_app.utils.requests_utils.ssl import (
            check_ssl_certificates_dir_setting,
        )

        """When the app is ready, run the discovery and init the indexes."""
        if "migrate" not in sys.argv:
            _check_settings()
            check_ssl_certificates_dir_setting(SSL_CERTIFICATES_DIR)
            discover.init_rules(self.apps)
            discover.create_public_workspace()
            discover.init_mongo_indexing()


def _check_settings():
    """Check settings

    Returns:

    """
    from core_main_app.commons.exceptions import CoreError

    # check celery settings
    if (
        settings.CELERYBEAT_SCHEDULER
        != "django_celery_beat.schedulers:DatabaseScheduler"
    ):
        raise CoreError(
            "CELERYBEAT_SCHEDULER setting needs to be set "
            "to 'django_celery_beat.schedulers:DatabaseScheduler'."
        )
