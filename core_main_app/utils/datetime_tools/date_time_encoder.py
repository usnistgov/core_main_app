"""
Encode the date correctly for Django password
"""

from datetime import datetime
from json import JSONEncoder


class DateTimeEncoder(JSONEncoder):
    """Instead of letting the default encoder convert datetime to string,
    convert datetime objects into a dict, which can be decoded by the
    DateTimeDecoder
    """

    def default(self, obj):
        """

        Args:
            obj:

        Returns:

        """
        if isinstance(obj, datetime):
            return {
                "__type__": "datetime",
                "year": obj.year,
                "month": obj.month,
                "day": obj.day,
                "hour": obj.hour,
                "minute": obj.minute,
                "second": obj.second,
                "microsecond": obj.microsecond,
            }

        return JSONEncoder.default(self, obj)
