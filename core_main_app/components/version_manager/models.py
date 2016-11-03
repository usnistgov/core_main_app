"""
Version Manager model
"""
from django_mongoengine import fields, Document


# TODO: could change versions to ReferenceField (Document?)
# TODO: could make current an IntField (index of the current in versions)
# TODO: could make is_disabled a Status with other possible values taken from an enum
class VersionManager(Document):
    """Manages versions"""
    title = fields.StringField(unique=True)
    user = fields.StringField(blank=True)
    versions = fields.ListField()
    current = fields.StringField()
    is_disabled = fields.BooleanField(default=False)
    disabled_versions = fields.ListField(default=[], blank=True)

    meta = {'allow_inheritance': True}

    def update_title(self, title):
        """
        Update the title associated to
        :param title:
        :return:
        """
        self.update(set__title=title)
        self.save()

    def disable(self):
        """
        Disable the Version Manager
        :return:
        """
        self.is_disabled = True
        self.save()

    def restore(self):
        """
        Restore the Version Manager
        :return:
        """
        self.is_disabled = False
        self.save()

    def disable_version(self, version_id):
        """
        Disable a version
        :param version_id:
        :return:
        """
        self.disabled_versions.append(str(version_id))
        self.save()

    def restore_version(self, version_id):
        """
        Restore a version
        :param version_id:
        :return:
        """
        del self.disabled_versions[self.disabled_versions.index(str(version_id))]
        self.save()

    def set_current_version(self, version_id):
        """
        Set the current version
        :param version_id:
        :return:
        """
        self.current = str(version_id)
        self.save()

    def get_version_number(self, version_id):
        """
        Return version number from version id
        :param version_id:
        :return:
        """
        return self.versions.index(version_id) + 1

    def insert(self, version):
        """
        Insert a version in the Version Manager
        :param version:
        :return:
        """
        self.versions.append(str(version.id))
        self.save()

    def _init(self, title, version, user=None):
        """
        Initialize the Version Manager
        :param title:
        :param version:
        :param user:
        :return:
        """
        self.title = title
        self.user = user
        self.versions = [str(version.id)]
        self.current = str(version.id)

    @staticmethod
    def get_all_version_managers():
        """
        Return all Version Managers
        :return:
        """
        return VersionManager.objects()

    @staticmethod
    def get_version_managers_filtered(disabled):
        """
        Return filtered list of Version Managers
        :param disabled:
        :return:
        """
        if disabled is not None:
            return VersionManager.objects(is_disabled=disabled)
        else:
            return VersionManager.objects()

    @staticmethod
    def get_by_id(version_manager_id):
        """
        Return Version Managers by id
        :param version_manager_id:
        :return:
        """
        return VersionManager.objects.get(pk=str(version_manager_id))

    @staticmethod
    def get_global_versions():
        """
        Return all Version Managers with user set to None
        :return:
        """
        return [vm for vm in VersionManager.objects() if vm.user is None]
