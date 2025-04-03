""" Signals to attach to Blob for processing.
"""

import logging

from django.db.models import signals as models_signals

from core_main_app.commons.exceptions import ApiError
from core_main_app.components.blob.models import Blob
from core_main_app.components.blob_processing_module import (
    tasks as blob_processing_module_tasks,
)
from core_main_app.components.blob_processing_module.models import (
    BlobProcessingModule,
)

logger = logging.getLogger(__name__)


def connect():
    """Connect signal for blob processing module"""
    models_signals.post_save.connect(post_save_blob, sender=Blob)
    models_signals.pre_delete.connect(pre_delete_blob, sender=Blob)
    logger.info("Registered signals for blob processing modules")


def post_save_blob(sender, instance, **kwargs):
    """Signal triggered after saving blob

    Args:
        sender:
        instance:
        kwargs:
    """
    try:
        logger.debug("Executing post save blob processing modules...")

        processing_module_strategy = (
            BlobProcessingModule.RUN_ON_CREATE
            if kwargs.get("created", False)
            else BlobProcessingModule.RUN_ON_UPDATE
        )

        blob_processing_module_tasks.process_blob_with_all_modules.apply_async(
            (
                instance.pk,
                processing_module_strategy,
                instance.user_id,
            )
        )
    except Exception as exc:
        raise ApiError(str(exc))


def pre_delete_blob(sender, instance, **kwargs):
    """Signal triggered before deleting blob

    Args:
        sender:
        instance:
        kwargs:
    """
    logger.debug("Starting blob processing modules on delete")

    blob_processing_module_tasks.process_blob_with_all_modules.apply_async(
        (
            instance.pk,
            BlobProcessingModule.RUN_ON_DELETE,
            instance.user_id,
        )
    )
