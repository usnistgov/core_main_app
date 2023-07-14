""" Templatetags to parse date string and convert to datetime object
"""
from datetime import datetime

from django import template
from django.utils import dateparse

register = template.Library()


@register.filter(name="parse_date")
def parse_date(value):
    """Parse date string

    Args:
        value: date string

    Returns: datetime
    """
    if isinstance(value, datetime):
        return value
    try:
        return dateparse.parse_datetime(value)
    except ValueError:
        return None
