""" Datetime utils
"""

from django.utils import timezone
import datetime
import iso8601


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


def datetime_to_utc_datetime_iso8601(raw_datetime, as_day=False):
    """Convert a datetime into its iso8601 UTC date.

    Parameters:
        raw_datetime: Datetime to convert.
        as_day: Returns the date without hours, minutes and seconds.

    Returns:
        Converted date (string).

    """
    # Ignore microseconds.
    raw_datetime = raw_datetime.replace(microsecond=0, tzinfo=None)
    datetime_format = "%Y-%m-%d" if as_day else "%Y-%m-%dT%H:%M:%SZ"

    return raw_datetime.strftime(datetime_format)


def utc_datetime_iso8601_to_datetime(utc_datetime):
    """Convert an iso8601 UTC date into datetime.

    Parameters:
        utc_datetime: iso8601 UTC date to convert.

    Returns:
        Converted date (Datetime).
    """
    return iso8601.parse_date(utc_datetime).replace(
        tzinfo=datetime.timezone.utc
    )
