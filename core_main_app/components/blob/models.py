""" Blob model
"""
from mongoengine import errors as mongoengine_errors
from mongoengine.queryset.base import NULLIFY

from blob_utils.blob_host_factory import BLOBHostFactory
from core_main_app.commons import exceptions
from core_main_app.components.workspace.models import Workspace
from core_main_app.settings import (
    BLOB_HOST,
    BLOB_HOST_URI,
    BLOB_HOST_USER,
    BLOB_HOST_PASSWORD,
)
from core_main_app.utils.validation.regex_validation import not_empty_or_whitespaces
from django_mongoengine import fields, Document


class Blob(Document):
    """Blob object"""

    filename = fields.StringField(blank=False, validation=not_empty_or_whitespaces)
    handle = fields.StringField(blank=False)
    user_id = fields.StringField(blank=False)
    workspace = fields.ReferenceField(
        Workspace, reverse_delete_rule=NULLIFY, blank=True
    )

    _blob_host = None
    _blob = None

    @staticmethod
    def get_by_id(blob_id):
        """Return the object with the given id.

        Args:
            blob_id:

        Returns:
            Blob

        """
        try:
            return Blob.objects.get(pk=str(blob_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all():
        """Return all blobs.

        Args:

        Returns:
            List of Blob instances.

        """
        return Blob.objects.all()

    @staticmethod
    def get_all_by_user_id(user_id):
        """Return all blobs by user.

        Args:
            user_id: User id.

        Returns:
            List of Blob instances for the given user id.

        """
        return Blob.objects(user_id=str(user_id)).all()

    @staticmethod
    def get_all_by_workspace(workspace):
        """Get all blobs that belong to the workspace.

        Args:
            workspace:

        Returns:

        """
        return Blob.objects(workspace=workspace).all()

    @staticmethod
    def get_all_by_list_workspace(list_workspace):
        """Get all blobs that belong to the list of workspace.

        Args:
            list_workspace:

        Returns:

        """
        return Blob.objects(workspace__in=list_workspace).all()

    @staticmethod
    def get_none():
        """Return None object, used by blobs.

        Returns:

        """
        return Blob.objects().none()

    @classmethod
    def blob_host(cls):
        """Return blob host.

        Returns:

        """
        if cls._blob_host is None:
            blob_host_factory = BLOBHostFactory(
                blob_host=BLOB_HOST,
                blob_host_uri=BLOB_HOST_URI,
                blob_host_user=BLOB_HOST_USER,
                blob_host_password=BLOB_HOST_PASSWORD,
            )
            cls._blob_host = blob_host_factory.create_blob_host()
        return cls._blob_host

    @property
    def blob(self):
        """Return blob from blob host.

        Returns:

        """
        # if the blob is not set
        if self._blob is None:
            # if an handle is set
            if self.handle is not None:
                # get the blob using its handle
                self._blob = Blob.blob_host().get(self.handle)
        return self._blob

    @blob.setter
    def blob(self, value):
        """Set blob value.

        Args:
            value: file

        Returns:

        """
        self._blob = value

    def save_blob(self):
        """Save blob on the blob host.

        Returns:

        """
        self.handle = str(Blob.blob_host().save(self._blob))

    def delete_blob(self):
        """Delete blob on the blob host.

        Returns:

        """
        Blob.blob_host().delete(self.handle)
