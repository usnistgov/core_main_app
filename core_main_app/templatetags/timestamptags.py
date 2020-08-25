"""Template tag to print date
"""
import pytz
from bson.objectid import ObjectId
from django import template

register = template.Library()


@register.filter
def print_datetime_utc_unaware(datetime):
    """Print datetime utc.

    Args:
        datetime: datetime timezone unaware

    Returns:

    """
    return datetime.replace(tzinfo=pytz.UTC)


@register.filter
def print_datetime_from_object_id(object_id):
    """Print timestamp.

    Args:
        object_id:

    Returns:

    """
    return _get_datetime(object_id)


def _get_datetime(object_id):
    """Return datetime from object id

    Args:
        object_id:

    Returns:

    """
    object_id = ObjectId(object_id)
    return object_id.generation_time
