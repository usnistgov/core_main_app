"""
Decode the date correctly for Django password
"""

import json
from datetime import datetime
from json import JSONDecoder

from django.utils import timezone

from core_main_app import settings


class DateTimeDecoder(json.JSONDecoder):
    """Date Time Decoder"""

    def __init__(self, *args, **kargs):
        """

        Args:
            *args:
            **kargs:
        """
        JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kargs)

    def dict_to_object(self, dictionary):
        """dict_to_object

        Args:
            dictionary:

        Returns:

        """
        if "__type__" not in dictionary:
            return dictionary

        type = dictionary.pop("__type__")
        try:
            if settings.USE_TZ:
                # timeit shows that datetime.now(tz=utc) is 24% slower
                date_obj = timezone.make_aware(datetime(**dictionary), timezone.utc)
            else:
                return datetime(**dictionary)

            return date_obj
        except:
            dictionary["__type__"] = type
            return dictionary
