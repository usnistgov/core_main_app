"""
Template Version Manager model
"""
from core_main_app.components.version_manager.models import VersionManager


class TemplateVersionManager(VersionManager):
    """Manages versions of templates"""

    @staticmethod
    def get_global_version_managers():
        """Returns all template version managers with user set to None

        Returns:

        """
        return super(TemplateVersionManager, TemplateVersionManager).get_global_version_managers()
