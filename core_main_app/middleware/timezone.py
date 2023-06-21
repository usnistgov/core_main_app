""" Timezone Middleware
"""
import pytz

from django.utils import timezone


class TimezoneMiddleware:
    """TimezoneMiddleware"""

    def __init__(self, get_response):
        """Init middleware

        Args:
            get_response:
        """
        self.get_response = get_response

    def __call__(self, request):
        """Call Middleware

        Args:
            request:

        Returns:

        """
        tzname = request.session.get("django_timezone")
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
