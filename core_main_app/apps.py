""" Apps file for setting core package when app is ready.
"""

from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate

from core_main_app import settings as main_settings


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
        _init_blob_modules_signals()


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

    if "allauth" in settings.INSTALLED_APPS:
        if (
            settings.ACCOUNT_ADAPTER
            != "core_main_app.utils.allauth.cdcs_adapter.CDCSAccountAdapter"
        ):
            raise CoreError(
                "ACCOUNT_ADAPTER needs to be set to "
                "'core_main_app.utils.allauth.cdcs_adapter.CDCSAccountAdapter'."
            )

        if "core_website_app" not in settings.INSTALLED_APPS:
            raise CoreError(
                "core_website_app is required to use allauth with CDCS."
            )

        if (
            settings.ACCOUNT_FORMS["signup"]
            != "core_main_app.utils.allauth.forms.CoreAccountSignupForm"
        ):
            raise CoreError(
                "ACCOUNT_FORMS['signup'] needs to be set to "
                "'core_main_app.utils.allauth.forms.CoreAccountSignupForm'."
            )

        if (
            settings.SOCIALACCOUNT_FORMS["signup"]
            != "core_main_app.utils.allauth.forms.CoreSocialAccountSignupForm"
        ):
            raise CoreError(
                "SOCIALACCOUNT_FORMS['signup'] needs to be set to "
                "'core_main_app.utils.allauth.forms.CoreSocialAccountSignupForm'."
            )


def _init_blob_modules_signals():
    """Initialize blob modules signals

    Returns:

    """
    from core_main_app.components.blob_processing_module import signals

    if main_settings.ENABLE_BLOB_MODULES_SIGNALS:
        signals.connect()
