"""
Workspace model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES


class Workspace(models.Model):
    """
    Workspace class.
    """

    title = models.CharField(
        blank=False,
        validators=[
            RegexValidator(
                regex=NOT_EMPTY_OR_WHITESPACES,
                message="Title must not be empty or only whitespaces",
                code="invalid_title",
            ),
        ],
        max_length=200,
    )
    owner = models.CharField(blank=True, max_length=200, null=True)
    read_perm_id = models.CharField(blank=False, max_length=200)
    write_perm_id = models.CharField(blank=False, max_length=200)
    is_public = models.BooleanField(default=False)

    def clean(self):
        """

        Returns:
        """
        # Check the title
        if (
            self.owner is not None
            and self.title.lower() == "global public workspace"
        ):
            raise exceptions.ModelError(
                "You can't create a workspace with the title: " + self.title
            )

    @staticmethod
    def get_all():
        """Get all workspaces.

        Returns:

        """
        return Workspace.objects.all()

    @staticmethod
    def get_all_by_owner(user_id):
        """Get all workspaces created by the given user id.

        Args:
            user_id

        Returns:

        """
        return Workspace.objects.filter(owner=str(user_id)).all()

    @staticmethod
    def get_by_id(workspace_id):
        """Return the workspace with the given id.

        Args:
            workspace_id

        Returns:
            Workspace (obj): Workspace object with the given id

        """
        try:
            return Workspace.objects.get(pk=workspace_id)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all_workspaces_with_read_access_by_user_id(
        user_id, read_permissions
    ):
        """Get all workspaces with read access for the given user id.

        Args:
            user_id
            read_permissions

        Returns:

        """
        return Workspace.objects.filter(
            Q(owner=str(user_id))
            | Q(read_perm_id__in=read_permissions)
            | Q(is_public=True)
        ).all()

    @staticmethod
    def get_all_workspaces_with_write_access_by_user_id(
        user_id, write_permissions
    ):
        """Get all workspaces with write access for the given user id.

        Args:
            user_id
            write_permissions

        Returns:

        """
        return Workspace.objects.filter(
            Q(owner=str(user_id)) | Q(write_perm_id__in=write_permissions)
        ).all()

    @staticmethod
    def get_all_workspaces_with_read_access_not_owned_by_user_id(
        user_id, read_permissions
    ):
        """Get all workspaces with read access not owned by the given user id.

        Args:
            user_id
            read_permissions

        Returns:

        """

        return Workspace.objects.filter(
            Q(read_perm_id__in=read_permissions) | Q(is_public=True),
            owner__ne=str(user_id),
        ).all()

    @staticmethod
    def get_all_workspaces_with_write_access_not_owned_by_user_id(
        user_id, write_permissions
    ):
        """Get all workspaces with write access not owned by the given user id.

        Args:
            user_id
            write_permissions

        Returns:

        """
        return Workspace.objects.filter(
            owner__ne=str(user_id), write_perm_id__in=write_permissions
        ).all()

    @staticmethod
    def get_all_public_workspaces():
        """Get all public workspaces.

        Args:

        Returns:

        """
        return Workspace.objects.filter(is_public=True).all()

    @staticmethod
    def get_all_other_public_workspaces(user_id):
        """Get all other public workspaces.

        Args:
            user_id

        Returns:

        """
        return Workspace.objects.filter(
            owner__ne=str(user_id), is_public=True
        ).all()

    @staticmethod
    def get_non_public_workspace_owned_by_user_id(user_id):
        """Get the non public workspaces owned by the given user id.

        Args:
            user_id

        Returns:

        """
        return Workspace.objects.filter(
            owner=str(user_id), is_public=False
        ).all()

    @staticmethod
    def get_public_workspaces_owned_by_user_id(user_id):
        """Get the public workspaces owned the given user id.

        Args:
            user_id

        Returns:

        """
        return Workspace.objects.filter(
            owner=str(user_id), is_public=True
        ).all()

    @staticmethod
    def get_global_workspace():
        """Get global workspace.

        Returns:
        """
        try:
            return Workspace.objects.get(owner=None, is_public=True)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @property
    def is_global(self):
        """Get is global.

        Returns:
        """
        return self.is_public and self.owner is None

    def __str__(self):
        """Workspace object as string

        Returns:

        """
        return self.title
