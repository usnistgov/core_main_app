""" Signals to attach to Data for processing.
"""

import logging

from django.db.models import signals as models_signals

from core_main_app.commons.exceptions import ApiError
from core_main_app.components.data.models import Data
from core_main_app.components.data_processing_module import (
    tasks as data_processing_module_tasks,
)
from core_main_app.components.data_processing_module.models import (
    DataProcessingModule,
)

logger = logging.getLogger(__name__)


def connect():
    """Connect signal for data processing module"""
    models_signals.post_save.connect(post_save_data, sender=Data)
    models_signals.pre_delete.connect(pre_delete_data, sender=Data)
    logger.info("Registered signals for data processing modules")


def post_save_data(sender, instance, **kwargs):
    """Signal triggered after saving data

    Args:
        sender:
        instance:
        kwargs:
    """
    try:
        logger.debug("Executing post save data processing modules...")

        processing_module_strategy = (
            DataProcessingModule.RUN_ON_CREATE
            if kwargs.get("created", False)
            else DataProcessingModule.RUN_ON_UPDATE
        )

        data_processing_module_tasks.process_data_with_all_modules.apply_async(
            (
                instance.pk,
                processing_module_strategy,
                instance.user_id,
            )
        )
    except Exception as exc:
        raise ApiError(str(exc))


def pre_delete_data(sender, instance, **kwargs):
    """Signal triggered before deleting data

    Args:
        sender:
        instance:
        kwargs:
    """
    logger.debug("Starting data processing modules on delete")

    data_processing_module_tasks.process_data_with_all_modules.apply_async(
        (
            instance.pk,
            DataProcessingModule.RUN_ON_DELETE,
            instance.user_id,
        )
    )
