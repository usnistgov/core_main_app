""" Apps file for setting core package when app is ready.
"""

from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def init_app(sender, **kwargs):
    """Initialize app

    Args:
        sender:
        **kwargs:

    Returns:

    """
    from core_main_app.permissions import discover

    discover.init_rules(sender.apps)
    discover.create_public_workspace()


class InitApp(AppConfig):
    """Core application settings."""

    verbose_name = "Core Main App"

    name = "core_main_app"
    """ :py:class:`str`: Package name
    """

    def ready(self):
        from core_main_app.settings import SSL_CERTIFICATES_DIR
        from core_main_app.utils.requests_utils.ssl import (
            check_ssl_certificates_dir_setting,
        )
        from core_main_app.permissions import discover

        _check_settings()
        check_ssl_certificates_dir_setting(SSL_CERTIFICATES_DIR)
        post_migrate.connect(init_app, sender=self)
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
