"""
Template Version Manager model
"""

from django.core.exceptions import ObjectDoesNotExist

from core_main_app.commons import exceptions
from core_main_app.components.version_manager.models import VersionManager


class TemplateVersionManager(VersionManager):
    """Manager of templates versions"""

    _class_name = "VersionManager.TemplateVersionManager"

    @property
    def class_name(self):
        return TemplateVersionManager._class_name

    @property
    def version_set(self):
        return self.template_set.all().order_by("pk")

    @staticmethod
    def get_by_id(version_manager_id):
        """Return Version Managers by id.

        Args:
            version_manager_id:

        Returns:

        """
        try:
            return TemplateVersionManager.objects.get(pk=version_manager_id)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_global_version_managers(_cls=True):
        """Return all Template Version Managers with user set to None.

        Returns:
            _cls: if True, restricts to TemplateVersionManager _cls
        """
        queryset = TemplateVersionManager.objects.filter(user=None).all()
        if _cls:
            queryset = queryset.filter(_cls=TemplateVersionManager._class_name).all()
        return queryset

    @staticmethod
    def get_active_global_version_manager(_cls=True):
        """Return all active Version Managers with user set to None.

        Returns:

        """
        queryset = TemplateVersionManager.objects.filter(
            is_disabled=False, user=None
        ).all()
        if _cls:
            queryset = queryset.filter(_cls=TemplateVersionManager._class_name).all()
        return queryset

    @staticmethod
    def get_active_version_manager_by_user_id(user_id, _cls=True):
        """Return all active Version Managers with given user id.

        Returns:

        """
        if not user_id:
            return TemplateVersionManager.objects.none()
        queryset = TemplateVersionManager.objects.filter(
            is_disabled=False, user=str(user_id)
        ).all()
        if _cls:
            queryset = queryset.filter(_cls=TemplateVersionManager._class_name).all()
        return queryset

    @staticmethod
    def get_all_version_manager_by_user_id(user_id, _cls=True):
        """Return all Version Managers with given user id.

        Args:
            user_id:
            _cls:

        Returns:

        """
        if not user_id:
            return TemplateVersionManager.objects.none()
        queryset = TemplateVersionManager.objects.filter(user=str(user_id)).all()
        if _cls:
            queryset = queryset.filter(_cls=TemplateVersionManager._class_name).all()
        return queryset

    @staticmethod
    def get_all_version_manager(_cls=True):
        """Return all Version Managers.

        Args:
            _cls:

        Returns:

        """
        queryset = TemplateVersionManager.objects.all()
        if _cls:
            queryset = queryset.filter(_cls=TemplateVersionManager._class_name).all()
        return queryset

    @staticmethod
    def get_by_id_list(list_id):
        """Return Version Managers with the given id list.

        Args:
            list_id:

        Returns:

        """
        return TemplateVersionManager.objects.filter(pk__in=list_id).all()

    def save_template_version_manager(self):
        """Custom save.

        Returns:
            Saved Instance.

        """
        super().save_version_manager()

    @staticmethod
    def get_active_global_version_manager_by_title(version_manager_title):
        """Return active Template Version Manager by its title with user set to None.

        Args:
            version_manager_title: Version Manager title

        Returns:
            Version Manager instance

        """
        try:
            return TemplateVersionManager.objects.get(
                is_disabled=False, title=version_manager_title, user=None
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))
