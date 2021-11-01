""" BLOB API
"""
import core_main_app.commons.exceptions as exceptions
from core_main_app.access_control.api import can_change_owner
from core_main_app.access_control.api import (
    has_perm_administration,
    can_read_or_write_in_workspace,
    can_read_id,
    can_write,
)
from core_main_app.access_control.decorators import access_control
from core_main_app.components.blob.access_control import (
    can_write_blob_workspace,
    can_write_blob,
)
from core_main_app.components.blob.models import Blob


@access_control(can_write_blob)
def insert(blob, user):
    """Insert the blob in the blob repository.

    Args:
        blob:
        user:

    Returns:

    """
    # if blob is not set
    if blob.blob is None:
        raise exceptions.ApiError("Unable to save the blob: blob field is not set.")
    # save blob on blob host
    blob.save_blob()
    # save blob in database
    return blob.save()


@access_control(can_write_blob_workspace)
def assign(blob, workspace, user):
    """Assign blob to a workspace.

    Args:
        blob:
        workspace:
        user:

    Returns:

    """
    blob.workspace = workspace
    return blob.save()


@access_control(can_write)
def delete(blob, user):
    """Delete the blob.

    Args:
        blob:

    Returns:

    """
    # delete blob on blob host
    blob.delete_blob()
    # delete blob in database
    return blob.delete()


@access_control(can_read_id)
def get_by_id(blob_id, user):
    """Return blob by its id.

    Args:
        blob_id:

    Returns:

    """
    return Blob.get_by_id(blob_id)


@access_control(has_perm_administration)
def get_all(user):
    """Return all blobs.

    Args:

    Returns:
        List of Blob instances.

    """
    return Blob.get_all()


def get_all_by_user(user):
    """Return all blobs by user.

    Args:
        user: User

    Returns:
        List of Blob instances for the given user id.

    """
    return Blob.get_all_by_user_id(str(user.id))


@access_control(can_read_or_write_in_workspace)
def get_all_by_workspace(workspace, user):
    """Get all data that belong to the workspace.

    Args:
        workspace:

    Returns:

    """
    return Blob.get_all_by_workspace(workspace)


@access_control(can_change_owner)
def change_owner(blob, new_user, user):
    """Change blob's owner.

    Args:
        blob:
        user:
        new_user:

    Returns:
    """
    # FIXME: user can transfer data to anybody, too permissive
    blob.user_id = str(new_user.id)
    blob.save()


def get_none():
    """Returns None object, used by blobs

    Returns:

    """
    return Blob.get_none()
