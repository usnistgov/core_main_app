""" Datetime utils
"""

from _datetime import datetime

import pytz


def datetime_now():
    """Return the current date

    Returns:

    """
    return datetime.now(pytz.utc)
