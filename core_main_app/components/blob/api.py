""" BLOB API
"""
import core_main_app.commons.exceptions as exceptions
from core_main_app.components.blob.models import Blob


def insert(blob):
    """ Insert the blob in the blob repository.

    Args:
        blob:

    Returns:

    """
    # if blob is not set
    if blob.blob is None:
        raise exceptions.ApiError("Unable to save the blob: blob field is not set.")
    # save blob on blob host
    blob.save_blob()
    # save blob in database
    return blob.save()


def delete(blob):
    """ Delete the blob.

    Args:
        blob:

    Returns:

    """
    # delete blob on blob host
    blob.delete_blob()
    # delete blob in database
    return blob.delete()


def get_by_id(blob_id):
    """ Return blob by its id.

    Args:
        blob_id:

    Returns:

    """
    return Blob.get_by_id(blob_id)


def get_all():
    """ Return all blobs.

    Args:

    Returns:
        List of Blob instances.

    """
    return Blob.get_all()


def get_all_by_user_id(user_id):
    """ Return all blobs by user.

    Args:
        user_id: User id.

    Returns:
        List of Blob instances for the given user id.

    """
    return Blob.get_all_by_user_id(user_id)


def get_all_except_user_id(user_id):
    """ Return all blobs except the ones of user.

    Args:
        user_id: User id.

    Returns:
        List of Blob instances except the given user id.

    """
    return Blob.get_all_except_user_id(user_id)
