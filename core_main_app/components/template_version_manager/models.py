"""
Template Version Manager model
"""
from core_main_app.components.version_manager.models import VersionManager


class TemplateVersionManager(VersionManager):
    """Manages versions of templates"""

    @staticmethod
    def create(title, version, user=None):
        """
        Create a new template version manager
        :param title:
        :param version:
        :param user:
        :return:
        """
        template_version_manager = TemplateVersionManager()
        template_version_manager._init(title, version, user)
        template_version_manager.save()
        return template_version_manager

    @staticmethod
    def get_global_versions():
        """
        Return all template version manager with user set to None
        :return:
        """
        return super(TemplateVersionManager, TemplateVersionManager).get_global_versions()
