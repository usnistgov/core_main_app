""" Apps file for setting core package when app is ready
"""
from django.apps import AppConfig
import core_main_app.permissions.discover as discover


class InitApp(AppConfig):
    """ Core application settings
    """
    name = 'core_main_app'

    def ready(self):
        """ Run when the app is ready.

        Returns:

        """
        discover.init_rules(self.apps)