"""
Version Manager model
"""
from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions


# TODO: could change versions to ReferenceField (Document?)
# TODO: could make current an IntField (index of the current in versions)
# TODO: could make is_disabled a Status with other possible values taken from an enum
class VersionManager(Document):
    """Manages versions"""
    title = fields.StringField(unique=True)
    user = fields.StringField(blank=True)
    versions = fields.ListField(default=[], blank=True)
    current = fields.StringField(blank=True)
    is_disabled = fields.BooleanField(default=False)
    disabled_versions = fields.ListField(default=[], blank=True)

    meta = {'allow_inheritance': True}

    def disable(self):
        """Disables the Version Manager

        Returns:

        """
        self.is_disabled = True

    def restore(self):
        """Restores the Version Manager

        Returns:

        """
        self.is_disabled = False

    def disable_version(self, version):
        """Disables a version

        Args:
            version:

        Returns:

        """
        self.disabled_versions.append(str(version.id))

    def restore_version(self, version):
        """Restores a version

        Args:
            version:

        Returns:

        """
        self.disabled_versions.remove(str(version.id))

    def set_current_version(self, version):
        """Sets the current version

        Args:
            version:

        Returns:

        """
        self.current = str(version.id)

    def get_version_number(self, version_id):
        """Returns version number from version id

        Args:
            version_id:

        Returns:

        Raises:
            DoesNotExist: Version does not exist.

        """
        try:
            return self.versions.index(str(version_id)) + 1
        except Exception as e:
            raise exceptions.DoesNotExist(e.message)

    def insert(self, version):
        """Inserts a version in the Version Manager

        Args:
            version:

        Returns:

        """
        self.versions.append(str(version.id))

    def get_disabled_versions(self):
        """Gets the list disabled versions of the version manager

        Returns:

        """
        return self.disabled_versions

    def get_version_by_number(self, version_number):
        """Returns the version by its version number.

        Args:
            version_number: Number of the version.

        Returns:

        Raises:
            DoesNotExist: Version does not exist.

        """
        try:
            return self.versions[version_number - 1]
        except Exception as e:
            raise exceptions.DoesNotExist(e.message)

    @staticmethod
    def get_all():
        """Returns all Version Managers

        Returns:

        """
        return VersionManager.objects.all()

    @staticmethod
    def get_all_filtered(disabled=False):
        """Returns filtered list of Version Managers

        Args:
            disabled:

        Returns:

        """
        return VersionManager.objects(is_disabled=disabled).all()

    @staticmethod
    def get_by_id(version_manager_id):
        """Returns Version Managers by id

        Args:
            version_manager_id:

        Returns:

        """
        try:
            return VersionManager.objects.get(pk=str(version_manager_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as e:
            raise exceptions.ModelError(e.message)

    @staticmethod
    def get_active_global_version_manager_by_title(version_manager_title):
        """Returns active Version Manager by its title with user set to None

        Args:
            version_manager_title: Version Manager title

        Returns:
            Version Manager instance

        """
        try:
            return VersionManager.objects.get(is_disabled=False, title=version_manager_title, user=None)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as e:
            raise exceptions.ModelError(e.message)

    @staticmethod
    def get_global_version_managers():
        """Returns all Version Managers with user set to None

        Returns:

        """
        return [vm for vm in VersionManager.objects.all() if vm.user is None]

    @staticmethod
    def get_active_global_version_manager():
        """ Returns all active Version Managers with user set to None

        Returns:

        """
        return [vm for vm in VersionManager.get_all_filtered(disabled=False) if vm.user is None]

    @staticmethod
    def get_disable_global_version_manager():
        """ Returns all disabled Version Managers with user set to None

        Returns:

        """
        return [vm for vm in VersionManager.get_all_filtered(disabled=True) if vm.user is None]

    @staticmethod
    def get_active_version_manager_by_user_id(user_id):
        """ Returns all active Version Managers with given user id

        Returns:

        """
        return VersionManager.objects(is_disabled=False, user=str(user_id)).all()

    @staticmethod
    def get_disable_version_manager_by_user_id(user_id):
        """ Returns all disabled Version Managers with given user id

        Returns:

        """
        return VersionManager.objects(is_disabled=True, user=str(user_id)).all()

    @staticmethod
    def get_all_version_manager_except_user_id(user_id):
        """ Returns all Version Managers of all users except user with given user id

        Args:
            user_id: user_id.

        Returns:

        """
        return VersionManager.objects(user__nin=str(user_id)).all()

    @staticmethod
    def get_all_version_manager_by_user_id(user_id):
        """ Returns all Version Managers with given user id

        Args:
            user_id: user_id.

        Returns:

        """
        return VersionManager.objects(user=str(user_id)).all()
