""" Apps file for setting core package when app is ready.
"""
import sys

from django.apps import AppConfig
from django.conf import settings

import core_main_app.permissions.discover as discover
from core_main_app.commons.exceptions import CoreError
from core_main_app.components.data.models import Data
from core_main_app.settings import SSL_CERTIFICATES_DIR
from core_main_app.utils.databases.mongoengine_database import init_text_index
from core_main_app.utils.requests_utils.ssl import check_ssl_certificates_dir_setting


class InitApp(AppConfig):
    """Core application settings."""

    name = "core_main_app"
    """ :py:class:`str`: Package name
    """

    def ready(self):
        """When the app is ready, run the discovery and init the indexes."""
        if "migrate" not in sys.argv:
            # check celery settings
            if (
                settings.CELERYBEAT_SCHEDULER
                != "django_celery_beat.schedulers:DatabaseScheduler"
            ):
                raise CoreError(
                    "CELERYBEAT_SCHEDULER setting needs to be set to 'django_celery_beat.schedulers:DatabaseScheduler'."
                )
            check_ssl_certificates_dir_setting(SSL_CERTIFICATES_DIR)
            discover.init_rules(self.apps)
            discover.create_public_workspace()
            init_text_index(Data)
