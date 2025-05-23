""" Celery tasks for blob processing modules.
"""

import logging
import re

from celery import shared_task
from django.contrib.auth.models import User

from core_main_app.commons.exceptions import ApiError
from core_main_app.components.blob import api as blob_api
from core_main_app.components.blob_processing_module import (
    api as blob_processing_module_api,
)

logger = logging.getLogger(__name__)


@shared_task
def process_blob_with_module(blob_module_id, blob_id, strategy, user_id=None):
    """Start the processing of a blob with a given module.

    Args:
        blob_module_id:
        blob_id:
        strategy:
        user_id:
    """
    if not user_id:
        error_message = "Cannot process blob without `user_id`"
        logger.error(error_message)
        raise ApiError(error_message)

    try:
        # Retrieve user, blob and blob_module
        user = User.objects.get(pk=user_id)

        blob = blob_api.get_by_id(blob_id, user)
        blob_module = blob_processing_module_api.get_by_id(
            blob_module_id, user
        )
        blob_module_class = blob_module.get_class()
    except Exception as exc:
        error_message = (
            f"An error occurred while instantiating blob module {blob_module_id} for "
            f"blob {blob_id} with user {user_id}: {str(exc)}"
        )
        logger.error(error_message)
        raise ApiError(error_message)

    if not re.match(blob_module.blob_filename_regexp, blob.filename):
        error_message = (
            f"File {blob.filename} cannot be processed by {blob_module.name}"
        )
        logger.error(error_message)
        raise ApiError(error_message)

    try:
        logger.info("File %s processed by %s", blob.filename, blob_module.name)
        return blob_module_class.process(
            blob, blob_module.parameters, strategy
        )
    except Exception as exc:
        error_message = f"File {blob.filename} cannot be processed by {blob_module.name}: {str(exc)}"
        logger.error(error_message)
        raise ApiError(error_message)


@shared_task
def process_blob_with_all_modules(blob_id, strategy, user_id=None):
    """Start the processing of a blob with a given module.

    Args:
        blob_id:
        strategy:
        user_id:
    """
    if not user_id:
        error_message = "Cannot process blob without `user_id`"
        logger.error(error_message)
        raise ApiError(error_message)

    logger.debug(
        f"Processing blob {str(blob_id)} with all modules for strategy {strategy} for user {str(user_id)}..."
    )

    try:
        # Retrieve user, blob and blob_module
        user = User.objects.get(pk=user_id)

        blob = blob_api.get_by_id(blob_id, user)
        blob_module_list = [
            blob_module
            for blob_module in blob_processing_module_api.get_all(user).filter(
                run_strategy_list__contains=strategy
            )
            if re.match(blob_module.blob_filename_regexp, blob.filename)
        ]
        logger.debug(
            "Found %d module(s) to execute for blob %d...",
            len(blob_module_list),
            blob_id,
        )
    except Exception as exc:
        error_message = (
            f"An error occurred while instantiating blob module list for "
            f"blob {blob_id} with user {user_id}: {str(exc)}"
        )
        logger.error(error_message)
        raise ApiError(error_message)

    for blob_module in blob_module_list:
        try:
            blob_module_class = blob_module.get_class()
            logger.debug(
                "Processing file %s with %s...",
                blob.filename,
                blob_module.name,
            )
            return blob_module_class.process(
                blob, blob_module.parameters, strategy
            )
        except Exception as exc:
            error_message = f"File {blob.filename} cannot be processed by {blob_module.name}: {str(exc)}"
            logger.error(error_message)
            raise ApiError(error_message)
