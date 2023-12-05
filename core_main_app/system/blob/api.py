""" System API for Blob objects.
"""
from core_main_app.components.blob.models import Blob


def get_by_id(blob_id):
    """Return blob by its id.

    Args:
        blob_id:

    Returns:

    """
    return Blob.get_by_id(blob_id)
