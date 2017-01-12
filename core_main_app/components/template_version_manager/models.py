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

    @staticmethod
    def get_active_global_version_manager():
        """ Returns all active Version Managers with user set to None

        Returns:

        """
        return super(TemplateVersionManager, TemplateVersionManager).get_active_global_version_manager()

    @staticmethod
    def get_disable_global_version_manager():
        """ Returns all disabled Version Managers with user set to None

        Returns:

        """
        return super(TemplateVersionManager, TemplateVersionManager).get_disable_global_version_manager()

    @staticmethod
    def get_active_version_manager_by_user_id(user_id):
        """ Returns all active Version Managers with given user id

        Returns:

        """
        return super(TemplateVersionManager, TemplateVersionManager).get_active_version_manager_by_user_id(user_id)

    @staticmethod
    def get_disable_version_manager_by_user_id(user_id):
        """ Returns all disabled Version Managers with given user id

        Returns:

        """
        return super(TemplateVersionManager, TemplateVersionManager).get_disable_version_manager_by_user_id(user_id)
