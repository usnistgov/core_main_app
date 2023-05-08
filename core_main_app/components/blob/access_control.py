""" Set of functions to define the rules for access control
"""
import logging

from django.conf import settings

from core_main_app.access_control.api import (
    has_perm_publish,
    can_write_in_workspace,
    check_can_write,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.data.access_control import (
    _get_read_accessible_workspaces_by_user,
)
from core_main_app.permissions import rights

logger = logging.getLogger(__name__)


def can_write_blob(func, blob, user):
    """Does the user has permission to write blob.

    Args:
        func:
        blob:
        user:

    Returns:

    """
    if user.is_anonymous:
        raise AccessControlError("Unable to insert blob if not authenticated.")

    return func(blob, user)


def has_perm_publish_blob(user):
    """Does the user have the permission to publish a blob.

    Args:
        user

    Returns
    """
    has_perm_publish(user, rights.PUBLISH_BLOB)


def can_write_blob_workspace(func, data, workspace, user):
    """Can user write data in workspace.

    Args:
        func:
        data:
        workspace:
        user:

    Returns:

    """
    return can_write_in_workspace(
        func, data, workspace, user, rights.PUBLISH_BLOB
    )


def can_write_metadata(func, blob, metadata, user):
    """Can user write metadata

    Args:
        func:
        blob:
        metadata:
        user:

    Returns:

    """
    check_can_write(blob, user)
    check_can_write(metadata, user)

    return func(blob, metadata, user)


def can_write_metadata_list(func, blob, metadata_list, user):
    """Can user write metadata list

    Args:
        func:
        blob:
        metadata_list:
        user:

    Returns:

    """
    check_can_write(blob, user)
    for metadata in metadata_list:
        check_can_write(metadata, user)

    return func(blob, metadata_list, user)


def filter_accessible_metadata(metadata, user):
    """Filter metadata to only return those that the user can read

    Args:
        metadata:
        user:

    Returns:

    """
    # If anon and not allowed to read data, return empty list
    if user is None or (
        user.is_anonymous and not settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT
    ):
        return []

    # If superuser, return unfiltered data
    if user.is_superuser:
        return metadata

    # Get list of workspace with read access
    accessible_workspaces = _get_read_accessible_workspaces_by_user(user)
    # Init list of metadata
    accessible_metadata = list()

    # Iterate through list of metadata
    for m in metadata:
        # If user is owner or can read metadata
        if str(m.user_id) == str(user.id) or (
            m.workspace is not None and m.workspace.id in accessible_workspaces
        ):
            # Add metadata to list
            accessible_metadata.append(m)

    return accessible_metadata
