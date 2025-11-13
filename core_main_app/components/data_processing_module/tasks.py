""" Celery tasks for data processing modules.
"""

import logging
import re

from celery import shared_task
from django.contrib.auth.models import User

from core_main_app.access_control.api import check_can_write
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.data import api as data_api
from core_main_app.components.data_processing_module import (
    api as data_processing_module_api,
)

logger = logging.getLogger(__name__)


@shared_task
def process_data_with_module(data_module_id, data_id, strategy, user_id=None):
    """Start the processing of a data with a given module.

    Args:
        data_module_id:
        data_id:
        strategy:
        user_id:
    """
    if not user_id:
        error_message = "Cannot process data without `user_id`"
        logger.error(error_message)
        raise ApiError(error_message)

    try:
        # Retrieve user, data and data_module
        user = User.objects.get(pk=user_id)
        data = data_api.get_by_id(data_id, user)
        check_can_write(data, user)
        data_module = data_processing_module_api.get_by_id(
            data_module_id, user
        )
        data_module_class = data_module.get_class()
    except Exception as exc:
        error_message = (
            f"An error occurred while instantiating data module {data_module_id} for "
            f"data {data_id} with user {user_id}: {str(exc)}"
        )
        logger.error(error_message)
        raise ApiError(error_message)

    try:
        logger.info("File %s processed by %s", data.title, data_module.name)
        return data_module_class.process(
            data, data_module.parameters, strategy
        )
    except Exception as exc:
        error_message = f"File {data.title} cannot be processed by {data_module.name}: {str(exc)}"
        logger.error(error_message)
        raise ApiError(error_message)


@shared_task
def process_data_with_all_modules(data_id, strategy, user_id=None):
    """Start the processing of a data with a given module.

    Args:
        data_id:
        strategy:
        user_id:
    """
    if not user_id:
        error_message = "Cannot process data without `user_id`"
        logger.error(error_message)
        raise ApiError(error_message)

    logger.debug(
        f"Processing data {str(data_id)} with all modules for strategy {strategy} for user {str(user_id)}..."
    )

    try:
        # Retrieve user, data and data_module
        user = User.objects.get(pk=user_id)
        data = data_api.get_by_id(data_id, user)
        check_can_write(data, user)

        data_module_list = [
            data_module
            for data_module in data_processing_module_api.get_all(user).filter(
                run_strategy_list__contains=strategy
            )
            if re.match(
                data_module.template_filename_regexp, data.template.filename
            )
        ]
        logger.debug(
            "Found %d module(s) to execute for data %d...",
            len(data_module_list),
            data_id,
        )
    except Exception as exc:
        error_message = (
            f"An error occurred while instantiating data module list for "
            f"data {data_id} with user {user_id}: {str(exc)}"
        )
        logger.error(error_message)
        raise ApiError(error_message)

    for data_module in data_module_list:
        try:
            data_module_class = data_module.get_class()
            logger.debug(
                "Processing file %s with %s...",
                data.title,
                data_module.name,
            )
            return data_module_class.process(
                data, data_module.parameters, strategy
            )
        except Exception as exc:
            error_message = f"File {data.title} cannot be processed by {data_module.name}: {str(exc)}"
            logger.error(error_message)
            raise ApiError(error_message)
