"""Template tag to print date
"""
from bson.objectid import ObjectId
from django import template
from dateutil import tz

register = template.Library()


@register.filter
def print_timestamp(object_id):
    """Print timestamp.

    Args:
        object_id:

    Returns:

    """
    return _get_datetime(object_id)


def _get_datetime(object_id, str_format="%m/%d/%Y %I:%M:%S %p"):
    """Return converted to UTC.

    Args:
        object_id:
        str_format:

    Returns:

    """
    object_id = ObjectId(object_id)
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    datetime_utc = object_id.generation_time
    datetime_utc = datetime_utc.replace(tzinfo=from_zone)
    datetime_local = datetime_utc.astimezone(to_zone)
    return datetime_local.strftime(str_format)
