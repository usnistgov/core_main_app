""" BLOB API
"""
import core_main_app.commons.exceptions as exceptions
from core_main_app.components.blob.models import Blob


def save(blob):
    """ Save the blob

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


def get_by_id(blob_id):
    """ Return blob by its id

    Args:
        blob_id:

    Returns:

    """
    return Blob.get_by_id(blob_id)
