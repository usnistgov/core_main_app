""" Utils for CDCS file storage
"""

from django.core.files.storage import default_storage

from core_main_app.commons.exceptions import CoreError
from core_main_app.settings import (
    GRIDFS_STORAGE,
    CUSTOM_FILE_STORAGE,
    UPLOAD_FOLDER_INCLUDES_USER,
)


def user_directory_path(instance, filename):
    """Build a custom upload directory path

    Args:
        instance:
        filename:

    Returns:

    """
    user_id = (
        getattr(instance, "user_id", None)
        if UPLOAD_FOLDER_INCLUDES_USER
        else None
    )

    if user_id:
        # file will be uploaded to MEDIA_ROOT/<model>/user_<id>/<filename>
        return f"{instance._meta.model_name}/user_{user_id}/{filename}"
    # file will be uploaded to MEDIA_ROOT/<model>/<filename>
    return f"{instance._meta.model_name}/{filename}"


def core_file_storage(model):
    """Return file storage

    Returns:

    """
    # check if custom storage selected for model
    if model in CUSTOM_FILE_STORAGE:
        # if GridFS storage
        if (
            CUSTOM_FILE_STORAGE[model]
            == "core_main_app.utils.storage.gridfs_storage.GridFSStorage"
        ):
            # check if GridFS storage is enabled
            if GRIDFS_STORAGE:
                # return GridFS storage if enabled
                from core_main_app.utils.storage.gridfs_storage import (
                    GridFSStorage,
                )

                return GridFSStorage(collection=model)
            else:
                # raise error if not enabled
                raise CoreError(
                    f"Set GRIDFS_STORAGE to True to enable this storage for model {model}."
                )
        else:
            # return selected storage
            return CUSTOM_FILE_STORAGE[model]

    # check if GridFS storage is enabled
    if GRIDFS_STORAGE:
        # return GridFS storage if enabled
        from core_main_app.utils.storage.gridfs_storage import GridFSStorage

        return GridFSStorage(collection=model)

    # if no storage settings, return default storage
    return default_storage
