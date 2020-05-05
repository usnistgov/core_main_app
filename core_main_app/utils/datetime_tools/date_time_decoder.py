"""
Decode the date correctly for Django password
"""

import json
from datetime import datetime
from json import JSONDecoder

from django.utils import timezone

from core_main_app import settings


class DateTimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kargs):
        """

        Args:
            *args:
            **kargs:
        """
        JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kargs)

    def dict_to_object(self, d):
        """

        Args:
            d:

        Returns:

        """
        if "__type__" not in d:
            return d

        type = d.pop("__type__")
        try:
            if settings.USE_TZ:
                # timeit shows that datetime.now(tz=utc) is 24% slower
                date_obj = timezone.make_aware(datetime(**d), timezone.utc)
            else:
                return datetime(**d)

            return date_obj
        except:
            d["__type__"] = type
            return d
