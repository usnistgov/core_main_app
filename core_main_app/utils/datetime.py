""" Datetime utils
"""
from django.utils import timezone


def datetime_now():
    """Returns the current date

    Returns:

    """
    return timezone.now()


def datetime_timedelta(**kwargs):
    """Returns a timedelta

    Returns:

    """
    return timezone.timedelta(**kwargs)
