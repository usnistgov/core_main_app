""" Blob Module API
"""

import logging
import re

from core_main_app.access_control.api import user_is_registered
from core_main_app.access_control.decorators import access_control
from core_main_app.components.blob import api as blob_api
from core_main_app.components.blob_processing_module.models import (
    BlobProcessingModule,
)

logger = logging.getLogger(__name__)


@access_control(user_is_registered)
def get_all(user):
    """Return all blob modules.

    Args:
        user:

    Returns:
        List of Blob Modules.
    """
    return BlobProcessingModule.get_all()


@access_control(user_is_registered)
def get_by_id(blob_module_id, user):
    """Retrieve blob module.

    Args:
        blob_module_id:
        user:

    Returns:
        Blob Module.
    """
    return BlobProcessingModule.get_by_id(blob_module_id)


@access_control(user_is_registered)
def get_all_by_blob_id(blob_id, user, run_strategy=None):
    """Retrieve a blob given a blob_id.

    Args:
        blob_id:
        user:
        run_strategy:

    Returns:
        Blob Module.
    """
    # Retrieve the blob (will check ownership) and blob modules.
    blob = blob_api.get_by_id(blob_id, user)
    blob_module_list = get_all(user)

    if run_strategy:  # Additional filtering if `run_strategy` is defined.
        blob_module_list = blob_module_list.filter(run_strategy=run_strategy)

    # Return the list of modules for which `blob_filename_regexp` matches the filename of
    #   the blob.
    return [
        blob_module
        for blob_module in blob_module_list
        if re.match(blob_module.blob_filename_regexp, blob.filename)
    ]
