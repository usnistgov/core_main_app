""" FileField utils
"""

import logging

logger = logging.getLogger(__name__)


def replace_file(sender, instance, **kwargs):
    """Replace existing file when object being updated

    Args:
        sender:
        instance:
        **kwargs:

    Returns:

    """
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.file and old_instance.file != instance.file:
            old_instance.file.delete(save=False)
    except sender.DoesNotExist as dne:
        logger.error(str(dne))
    except Exception as exc:
        logger.error(str(exc))
