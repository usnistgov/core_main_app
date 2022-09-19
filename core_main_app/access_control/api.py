""" Set of functions to define the common rules for access control across collections
"""
import logging

from django.contrib.auth.models import User

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.workspace import api as workspace_api
from core_main_app.permissions import api as permissions_api, rights as rights
from core_main_app.settings import (
    CAN_SET_PUBLIC_DATA_TO_PRIVATE,
    CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT,
)

logger = logging.getLogger(__name__)


def has_perm_publish(user, codename):
    """Does the user have the permission to publish.

    Args:
        user
        codename

    Returns
    """
    publish_perm = permissions_api.get_by_codename(codename)
    if not user.has_perm(
        publish_perm.content_type.app_label + "." + publish_perm.codename
    ):
        raise AccessControlError("The user doesn't have enough rights to publish.")


def has_perm_administration(func, *args, **kwargs):
    """Does the given user have administration rights.

    Args:
        func:
        *args:
        **kwargs:

    Returns:

    """
    try:
        user = next((arg for arg in args if isinstance(arg, User)), None)
        if user and user.is_superuser:
            return func(*args, **kwargs)
    except Exception as e:
        logger.warning(f"has_perm_administration threw an exception: {str(e)}")

    raise AccessControlError("The user doesn't have enough rights.")


def is_superuser(func, *args, **kwargs):
    """Is the user a superuser.

    Args:
        func:
        *args:
        **kwargs:

    Returns:

    """
    try:
        request = kwargs["request"]
        if request and request.user.is_superuser:
            return func(*args, **kwargs)
    except Exception as e:
        logger.warning(f"has_perm_administration threw an exception: {str(e)}")

    raise AccessControlError("The user doesn't have enough rights.")


def check_can_write(document, user):
    """Check that the user can write.

    Args:
        document:
        user:

    Returns:

    """
    # Raise error if anonymous user
    if user.is_anonymous:
        raise AccessControlError("Unable to write if not authenticated.")

    # TODO: data will inherit of workspace rights, which means a owner can't edit
    #  or delete a data if data in wkp that doesn't give hin write rights
    if hasattr(document, "workspace") and document.workspace is not None:
        if workspace_api.is_workspace_public(
            document.workspace
        ) and document.user_id == str(user.id):
            has_perm_publish(user, rights.PUBLISH_DATA)
        else:  # Workspace not public OR editing someone else's data.
            _check_can_write_in_workspace(document.workspace, user)

    # not the owner and workspace is not set or None
    if document.user_id != str(user.id) and (
        not hasattr(document, "workspace") or document.workspace is None
    ):
        raise AccessControlError("The user doesn't have enough rights.")


def check_can_read_list(document_list, user):
    """Check that the user can read each document of the list.

    Args:
        document_list:
        user:

    Returns:

    """
    if document_list.count() > 0:
        # exclude own data
        other_users_documents = document_list.exclude(user_id=str(user.id))

        # check that other users private data is not accessed
        other_users_private_document = other_users_documents.filter(
            workspace__isnull=True
        )
        if other_users_private_document.count() > 0:
            raise AccessControlError(
                "The user doesn't have enough rights to access this data"
            )

        # get list of accessible workspaces
        accessible_workspaces = [
            workspace.id
            for workspace in workspace_api.get_all_workspaces_with_read_access_by_user(
                user
            )
        ]
        # get list of all workspaces of returned data
        document_workspaces = set(
            other_users_documents.values_list("workspace", flat=True)
        )
        # check that accessed workspaces are in the list of accessible workspaces
        for workspace in document_workspaces:
            if workspace not in accessible_workspaces:
                raise AccessControlError(
                    "The user doesn't have enough rights to access this data"
                )


def can_write_document_in_workspace(func, document, workspace, user):
    """Can user write data in workspace.

    Args:
        func:
        document:
        workspace:
        user:

    Returns:

    """
    return can_write_in_workspace(func, document, workspace, user, rights.PUBLISH_DATA)


def can_read_or_write_in_workspace(func, workspace, user):
    """Can user read or write in workspace.

    Args:
        func:
        workspace:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(workspace, user)

    _check_can_read_or_write_in_workspace(workspace, user)
    return func(workspace, user)


def can_write_in_workspace(func, document, workspace, user, codename):
    """Can user write in workspace.

    Args:
        func:
        document:
        workspace:
        user:
        codename:

    Returns:

    """
    if user.is_superuser:
        return func(document, workspace, user)
    if workspace is not None:
        if workspace_api.is_workspace_public(workspace):
            has_perm_publish(user, codename)
        else:
            _check_can_write_in_workspace(workspace, user)

    check_can_write(document, user)

    # if we can not unpublish
    if CAN_SET_PUBLIC_DATA_TO_PRIVATE is False:
        # if document is in public workspace
        if document.workspace is not None and workspace_api.is_workspace_public(
            document.workspace
        ):
            # if target workspace is private
            if (
                workspace is None
                or workspace_api.is_workspace_public(workspace) is False
            ):
                raise AccessControlError("The document can not be unpublished.")

    return func(document, workspace, user)


def can_read(func, user):
    """Can a user read

    Args:
        func:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(user)

    # get list of document
    document_list = func(user)
    # check that the user can access the list of document
    check_can_read_list(document_list, user)
    # return list of document
    return document_list


def can_read_id(func, document_id, user):
    """Can read from object id.

    Args:
        func:
        document_id:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(document_id, user)

    document = func(document_id, user)
    _check_can_read(document, user)
    return document


def can_write(func, document, user):
    """Can user write

    Args:
        func:
        document:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(document, user)

    check_can_write(document, user)
    return func(document, user)


def can_request_write(func, document, request):
    """Can user request write

    Args:
        func:
        document:
        request:

    Returns:

    """
    if request.user.is_superuser:
        return func(document, request)

    check_can_write(document, request.user)
    return func(document, request)


def can_anonymous_access_public_data(func, *args, **kwargs):
    """Can anonymous access a public data

    Args:
        func:
        *args:
        **kwargs:

    Returns:

    """
    user = next((arg for arg in args if isinstance(arg, User)), None)

    _check_anonymous_access(user)
    return func(*args, **kwargs)


def _check_can_write_in_workspace(workspace, user):
    """Check that user can write in the workspace.

    Args:
        workspace:
        user:

    Returns:

    """
    accessible_workspaces = workspace_api.get_all_workspaces_with_write_access_by_user(
        user
    )
    if workspace not in accessible_workspaces:
        raise AccessControlError(
            "The user does not have the permission to write into this workspace."
        )


def _check_can_read_or_write_in_workspace(workspace, user):
    """Check that user can read or write in the workspace.

    Args:
        workspace:
        user:

    Returns:

    """
    accessible_write_workspaces = (
        workspace_api.get_all_workspaces_with_write_access_by_user(user)
    )
    accessible_read_workspaces = (
        workspace_api.get_all_workspaces_with_read_access_by_user(user)
    )
    if workspace not in list(accessible_write_workspaces) + list(
        accessible_read_workspaces
    ):
        raise AccessControlError(
            "The user does not have the permission to read or write into this workspace."
        )


def _check_anonymous_access(user):
    """Check anonymous access

    Args:
        user:

    Returns:
    """
    if (user is None or user.is_anonymous) and not CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
        raise AccessControlError(
            "The user doesn't have enough rights to access this document."
        )


def _check_can_read(document, user):
    """Check that the user can read.

    Args:
        document:
        user:

    Returns:

    """
    _check_anonymous_access(user)

    # workspace case
    if document.user_id != str(user.id):
        # workspace is set
        if hasattr(document, "workspace") and document.workspace is not None:
            # get list of accessible workspaces
            accessible_workspaces = (
                workspace_api.get_all_workspaces_with_read_access_by_user(user)
            )
            # check that accessed document belongs to an accessible workspace
            if document.workspace not in accessible_workspaces:
                raise AccessControlError(
                    "The user doesn't have enough rights to access this."
                )
        # workspace is not set
        else:
            raise AccessControlError(
                "The user doesn't have enough rights to access this document."
            )


def can_change_owner(func, document, new_user, user):
    """Can user change document's owner.

    Args:
        func:
        document:
        new_user:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(document, new_user, user)

    if document.user_id != str(user.id):
        raise AccessControlError(
            "The user doesn't have enough rights to access this document."
        )

    return func(document, new_user, user)
