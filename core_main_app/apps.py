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

    if (
        "allauth" in settings.INSTALLED_APPS
        and settings.ALLAUTH_ACCOUNT_REQUESTS_FOR_NEW_USERS
    ):
        if (
            settings.ACCOUNT_ADAPTER
            != "core_main_app.utils.allauth.cdcs_adapter.CDCSAccountAdapter"
        ):
            raise CoreError(
                "ACCOUNT_ADAPTER needs to be set to "
                "'core_main_app.utils.allauth.cdcs_adapter.CDCSAccountAdapter'."
            )

        if settings.SOCIALACCOUNT_AUTO_SIGNUP:
            raise CoreError(
                "SOCIALACCOUNT_AUTO_SIGNUP needs to be set to False."
            )

        if "core_website_app" not in settings.INSTALLED_APPS:
            raise CoreError("core_website_app is required to use allauth.")

        if (
            settings.ACCOUNT_SIGNUP_FORM_CLASS
            != "core_main_app.utils.allauth.forms.CoreSignupForm"
        ):
            raise CoreError(
                "ACCOUNT_SIGNUP_FORM_CLASS needs to be set to "
                "'core_main_app.utils.allauth.forms.CoreSignupForm'."
            )
