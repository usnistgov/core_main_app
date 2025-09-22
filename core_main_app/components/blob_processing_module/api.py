""" Blob Processing Module API
"""

import logging
import re

from core_main_app.access_control.api import user_is_registered, user_is_staff
from core_main_app.access_control.decorators import access_control
from core_main_app.components.blob import api as blob_api
from core_main_app.components.blob_processing_module.models import (
    BlobProcessingModule,
)

logger = logging.getLogger(__name__)


@access_control(user_is_registered)
def get_all(user):  # noqa
    """Return all blob processing modules.

    Args:
        user: The user object requesting the list (used for access control).

    Returns:
        list: A list or QuerySet of all BlobProcessingModule instances.
    """
    return BlobProcessingModule.get_all()


@access_control(user_is_registered)
def get_by_id(blob_module_id, user):  # noqa
    """Retrieve a specific blob processing module by its ID.

    Args:
        blob_module_id: The unique identifier of the module to retrieve.
        user: The user object requesting the module (used for access control).

    Returns:
        BlobProcessingModule: The requested module instance.
    """
    return BlobProcessingModule.get_by_id(blob_module_id)


@access_control(user_is_registered)
def get_all_by_blob_id(blob_id, user, run_strategy=None):
    """Retrieve all blob processing modules applicable to a specific blob.

    This function fetches the blob (checking user ownership), filters modules
    by the optional run strategy, and then returns only the modules where the
    module's filename regex matches the blob's filename.

    Args:
        blob_id: The unique identifier of the target blob.
        user: The user object requesting the modules (used for blob access check).
        run_strategy (str, optional): A specific execution strategy to filter
            the modules by. Defaults to None.

    Returns:
        list: A list of BlobProcessingModule instances that match the blob's
        filename pattern and the optional run strategy.
    """
    # Retrieve the blob (will check ownership) and blob modules.
    blob = blob_api.get_by_id(blob_id, user)
    blob_module_list = get_all(user)

    # Additional filtering if `run_strategy` is defined.
    blob_module_list = (
        list(
            blob_module_list.filter(run_strategy_list__contains=run_strategy)
        )  # noqa
        if run_strategy
        else blob_module_list
    )

    # Return the list of modules for which `blob_filename_regexp` matches the filename of
    #   the blob.
    return [
        blob_module
        for blob_module in blob_module_list
        if re.match(blob_module.blob_filename_regexp, blob.filename)
    ]


@access_control(user_is_staff)
def delete(blob_module_id, user):  # noqa
    """Deletes a BlobProcessingModule instance identified by the given ID.

    Args:
        blob_module_id: The unique identifier of the BlobProcessingModule to delete.
        user: The user object requesting the deletion (checked for staff status).

    Returns:
        The result of the delete operation on the module instance.
    """
    return BlobProcessingModule.get_by_id(blob_module_id).delete()
