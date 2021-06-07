"""
Version Manager model
"""
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions
from core_main_app.utils.validation.regex_validation import not_empty_or_whitespaces
from django_mongoengine import fields, Document


# TODO: could change versions to ReferenceField (Document?)
# TODO: could make current an IntField (index of the current in versions)
# TODO: could make is_disabled a Status with other possible values taken from an enum


class VersionManager(Document):
    """Version Manager"""

    title = fields.StringField(unique=True, validation=not_empty_or_whitespaces)
    user = fields.StringField(blank=True)
    versions = fields.ListField(default=[], blank=True)
    current = fields.StringField(blank=True)
    is_disabled = fields.BooleanField(default=False)
    disabled_versions = fields.ListField(default=[], blank=True)

    meta = {"allow_inheritance": True}

    def disable(self):
        """Disable the Version Manager.

        Returns:

        """
        self.is_disabled = True

    def restore(self):
        """Restore the Version Manager.

        Returns:

        """
        self.is_disabled = False

    def disable_version(self, version):
        """Disable a version.

        Args:
            version:

        Returns:

        """
        # check if the version is not already disabled
        if str(version.id) not in list(self.disabled_versions):
            self.disabled_versions.append(str(version.id))

    def restore_version(self, version):
        """Restore a version.

        Args:
            version:

        Returns:

        """
        self.disabled_versions.remove(str(version.id))

    def set_current_version(self, version):
        """Set the current version.

        Args:
            version:

        Returns:

        """
        self.current = str(version.id)

    def insert(self, version):
        """Insert a version in the Version Manager.

        Args:
            version:

        Returns:

        """
        self.versions.append(str(version.id))

    def get_disabled_versions(self):
        """Get the list disabled versions of the version manager.

        Returns:

        """
        return self.disabled_versions

    @staticmethod
    def get_all():
        """Return all Version Managers.

        Returns:

        """
        return VersionManager.objects.all()

    @staticmethod
    def get_by_id(version_manager_id):
        """Return Version Managers by id.

        Args:
            version_manager_id:

        Returns:

        """
        try:
            return VersionManager.objects.get(pk=str(version_manager_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_by_id_list(list_id):
        """Return Version Managers with the given id list.

        Args:
            list_id:

        Returns:

        """
        return VersionManager.objects(pk__in=list_id).all()

    @staticmethod
    def get_active_global_version_manager_by_title(version_manager_title):
        """Return active Version Manager by its title with user set to None.

        Args:
            version_manager_title: Version Manager title

        Returns:
            Version Manager instance

        """
        try:
            return VersionManager.objects.get(
                is_disabled=False, title=version_manager_title, user=None
            )
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_global_version_managers():
        """Return all Version Managers with user set to None.

        Returns:

        """
        return VersionManager.objects(user=None).all()

    @staticmethod
    def get_active_global_version_manager():
        """Return all active Version Managers with user set to None.

        Returns:

        """
        return VersionManager.objects(is_disabled=False, user=None).all()

    @staticmethod
    def get_active_version_manager_by_user_id(user_id):
        """Return all active Version Managers with given user id.

        Returns:

        """
        return VersionManager.objects(is_disabled=False, user=str(user_id)).all()

    @staticmethod
    def get_all_version_manager_except_user_id(user_id):
        """Return all Version Managers of all users except user with given user id.

        Args:
            user_id: user_id.

        Returns:

        """
        return VersionManager.objects(user__nin=str(user_id)).all()

    @staticmethod
    def get_all_version_manager_by_user_id(user_id):
        """Return all Version Managers with given user id.

        Args:
            user_id: user_id.

        Returns:

        """
        return VersionManager.objects(user=str(user_id)).all()

    def save_version_manager(self):
        """Custom save.

        Returns:
            Saved Instance.

        """
        try:
            return self.save()
        except mongoengine_errors.NotUniqueError as e:
            raise exceptions.NotUniqueError(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def clean(self):
        """Clean is called before saving

        Returns:

        """
        self.title = self.title.strip()
