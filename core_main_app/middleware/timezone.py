""" Timezone Middleware
"""

from django.utils import timezone

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.user_preferences import (
    api as user_preferences_api,
)

USER_TIMEZONE_NOT_SET = "NOT_SET"


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
        tz_name = request.session.get("django_timezone")
        if not tz_name and request.user.id:
            try:
                user_preferences = user_preferences_api.get_by_user(
                    request.user
                )
            except DoesNotExist:
                user_preferences = None
                # Set session to avoid fetching preferences again
                request.session["django_timezone"] = USER_TIMEZONE_NOT_SET
            if user_preferences:
                tz_name = user_preferences.timezone
                request.session["django_timezone"] = tz_name

        if tz_name and tz_name != USER_TIMEZONE_NOT_SET:
            timezone.activate(tz_name)
        else:
            timezone.deactivate()
        return self.get_response(request)
