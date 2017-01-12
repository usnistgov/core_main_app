"""
Template Version Manager model
"""
from core_main_app.components.version_manager.models import VersionManager


class TemplateVersionManager(VersionManager):
    """Manages versions of templates"""

    @staticmethod
    def get_global_version_managers(_cls=True):
        """Returns all Template Version Managers with user set to None

        Returns:
            _cls: if True, restricts to TemplateVersionManager _cls
        """
        if _cls:
            return [vm for vm in TemplateVersionManager.objects(_cls="VersionManager.TemplateVersionManager")
                .all() if vm.user is None]
        else:
            return [vm for vm in TemplateVersionManager.objects().all() if vm.user is None]

    # FIXME: do not query on all Version Managers
    @staticmethod
    def get_active_global_version_manager():
        """ Returns all active Version Managers with user set to None

        Returns:

        """
        return super(TemplateVersionManager, TemplateVersionManager).get_active_global_version_manager()

    # FIXME: do not query on all Version Managers
    @staticmethod
    def get_disable_global_version_manager():
        """ Returns all disabled Version Managers with user set to None

        Returns:

        """
        return super(TemplateVersionManager, TemplateVersionManager).get_disable_global_version_manager()

    # FIXME: do not query on all Version Managers
    @staticmethod
    def get_active_version_manager_by_user_id(user_id):
        """ Returns all active Version Managers with given user id

        Returns:

        """
        return super(TemplateVersionManager, TemplateVersionManager).get_active_version_manager_by_user_id(user_id)

    # FIXME: do not query on all Version Managers
    @staticmethod
    def get_disable_version_manager_by_user_id(user_id):
        """ Returns all disabled Version Managers with given user id

        Returns:

        """
        return super(TemplateVersionManager, TemplateVersionManager).get_disable_version_manager_by_user_id(user_id)
