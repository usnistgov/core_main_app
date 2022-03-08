""" Utils for CDCS file storage
"""
from django.core.files.storage import default_storage

from core_main_app.settings import GRIDFS_STORAGE


def user_directory_path(instance, filename):
    """Get path to user directory

    Args:
        instance:
        filename:

    Returns:

    """
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.user_id, filename)


def core_file_storage(model):
    """Return file storage

    Returns:

    """
    if GRIDFS_STORAGE:
        from core_main_app.utils.storage.gridfs_storage import GridFSStorage

        return GridFSStorage(collection=model)
    return default_storage
