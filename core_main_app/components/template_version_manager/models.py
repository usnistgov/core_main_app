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
        queryset = [vm for vm in TemplateVersionManager.objects().all() if vm.user is None]
        if _cls:
            return TemplateVersionManager._filter_by_cls(queryset)
        return queryset

    @staticmethod
    def get_active_global_version_manager(_cls=True):
        """ Returns all active Version Managers with user set to None

        Returns:

        """
        queryset = super(TemplateVersionManager, TemplateVersionManager).get_active_global_version_manager()
        if _cls:
            return TemplateVersionManager._filter_by_cls(queryset)
        return queryset

    @staticmethod
    def get_disable_global_version_manager(_cls=True):
        """ Returns all disabled Version Managers with user set to None

        Returns:

        """
        queryset = super(TemplateVersionManager, TemplateVersionManager).get_disable_global_version_manager()
        if _cls:
            return TemplateVersionManager._filter_by_cls(queryset)
        return queryset

    @staticmethod
    def get_active_version_manager_by_user_id(user_id, _cls=True):
        """ Returns all active Version Managers with given user id

        Returns:

        """
        queryset = super(TemplateVersionManager, TemplateVersionManager).get_active_version_manager_by_user_id(user_id)
        if _cls:
            return TemplateVersionManager._filter_by_cls(queryset)
        return queryset

    @staticmethod
    def get_disable_version_manager_by_user_id(user_id, _cls=True):
        """ Returns all disabled Version Managers with given user id

        Returns:

        """
        queryset = super(TemplateVersionManager, TemplateVersionManager).get_disable_version_manager_by_user_id(user_id)
        if _cls:
            return TemplateVersionManager._filter_by_cls(queryset)
        return queryset

    @staticmethod
    def get_all_by_version_ids(version_ids):
        """Gets all template version managers by a list of version ids.

        Args:
            version_ids: list of version ids.

        Returns:
            List of template version managers.

        """
        return TemplateVersionManager.objects(versions__in=version_ids).all()

    @staticmethod
    def _filter_by_cls(queryset):
        """

        Args:
            queryset:

        Returns:

        """
        return [record for record in queryset if record['_cls'] == 'VersionManager.TemplateVersionManager']

    @staticmethod
    def get_all_version_manager_except_user_id(user_id, _cls=True):
        """ Return all Version Managers of all users except user with given user id.

        Args:
            user_id:
            _cls:

        Returns:

        """
        queryset = super(TemplateVersionManager, TemplateVersionManager).get_all_version_manager_except_user_id(user_id)
        if _cls:
            return TemplateVersionManager._filter_by_cls(queryset)
        return queryset

    @staticmethod
    def get_all_version_manager_by_user_id(user_id, _cls=True):
        """ Return all Version Managers with given user id.

        Args:
            user_id:
            _cls:

        Returns:

        """
        queryset = super(TemplateVersionManager, TemplateVersionManager).get_all_version_manager_by_user_id(user_id)
        if _cls:
            return TemplateVersionManager._filter_by_cls(queryset)
        return queryset

