"""Template tag to print date
"""
from bson.objectid import ObjectId
from django import template

register = template.Library()


@register.filter
def print_timestamp(object_id):
    """ Print timestamp.

    Args:
        object_id:

    Returns:

    """
    return _get_datetime(object_id)


def _get_datetime(object_id):
    """ Return datetime from object id

    Args:
        object_id:

    Returns:

    """
    object_id = ObjectId(object_id)
    return object_id.generation_time
