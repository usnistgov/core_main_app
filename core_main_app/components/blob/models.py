""" Blob model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES
from core_main_app.components.workspace.models import Workspace
from core_main_app.utils.storage.storage import user_directory_path, core_file_storage


class Blob(models.Model):
    """Blob object"""

    filename = models.CharField(
        blank=False,
        validators=[
            RegexValidator(
                regex=NOT_EMPTY_OR_WHITESPACES,
                message="Filename must not be empty or only whitespaces",
                code="invalid_title",
            ),
        ],
        max_length=200,
    )
    user_id = models.CharField(blank=False, max_length=200)
    workspace = models.ForeignKey(
        Workspace, on_delete=models.SET_NULL, blank=True, null=True
    )
    blob = models.FileField(
        null=True,
        upload_to=user_directory_path,
        storage=core_file_storage(model="blob"),
    )

    creation_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_by_id(blob_id):
        """Return the object with the given id.

        Args:
            blob_id:

        Returns:
            Blob

        """
        try:
            return Blob.objects.get(pk=blob_id)
        except ObjectDoesNotExist as e:
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
        return Blob.objects.filter(user_id=str(user_id)).all()

    @staticmethod
    def get_all_by_workspace(workspace):
        """Get all blobs that belong to the workspace.

        Args:
            workspace:

        Returns:

        """
        return Blob.objects.filter(workspace=workspace).all()

    @staticmethod
    def get_all_by_list_workspace(list_workspace):
        """Get all blobs that belong to the list of workspace.

        Args:
            list_workspace:

        Returns:

        """
        return Blob.objects.filter(workspace__in=list_workspace).all()

    @staticmethod
    def get_none():
        """Return None object, used by blobs.

        Returns:

        """
        return Blob.objects.none()

    def __str__(self):
        """Blob object as string

        Returns:

        """
        return self.filename
