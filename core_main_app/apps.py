""" Apps file for setting core package when app is ready
"""
from django.apps import AppConfig

import core_main_app.permissions.discover as discover
from core_main_app.components.data.models import Data
from core_main_app.utils.databases.mongoengine_database import init_text_index


class InitApp(AppConfig):
    """ Core application settings
    """
    name = 'core_main_app'

    def ready(self):
        """ Run when the app is ready.

        Returns:

        """
        discover.init_rules(self.apps)
        discover.create_public_workspace()
        init_text_index(Data)
