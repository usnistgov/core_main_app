from unittest.mock import MagicMock, patch

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import SimpleTestCase, RequestFactory

from core_main_app.middleware.timezone import TimezoneMiddleware


class TestTimezoneMiddleware(SimpleTestCase):
    """TestTimezoneMiddleware"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()

    @patch("django.utils.timezone.activate")
    def test_timezone_middleware_set(self, timezone_activate):
        """test_timezone_middleware_set

        Returns:

        """
        # Arrange
        get_response = MagicMock()
        new_timezone = "UTC"
        request = self.factory.post("core_main_set_timezone")
        # Add middlewares
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session["django_timezone"] = new_timezone

        # Act
        middleware = TimezoneMiddleware(get_response)
        middleware(request)

        # Assert
        self.assertTrue(timezone_activate.called)

    @patch("django.utils.timezone.deactivate")
    def test_timezone_middleware_not_set(self, timezone_deactivate):
        """test_timezone_middleware_not_set

        Returns:

        """
        # Arrange
        get_response = MagicMock()
        request = self.factory.post("core_main_set_timezone")
        # Add middlewares
        middleware = SessionMiddleware()
        middleware.process_request(request)

        # Act
        middleware = TimezoneMiddleware(get_response)
        middleware(request)

        # Assert
        self.assertTrue(timezone_deactivate.called)
