"""Template tag to print date
"""
import pytz
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
