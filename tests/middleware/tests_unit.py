from unittest.mock import MagicMock, patch

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import SimpleTestCase, RequestFactory

from core_main_app.components.user_preferences.models import UserPreferences
from core_main_app.middleware.timezone import (
    TimezoneMiddleware,
    USER_TIMEZONE_NOT_SET,
)


class TestTimezoneMiddleware(SimpleTestCase):
    """TestTimezoneMiddleware"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    @patch("django.utils.timezone.activate")
    def test_timezone_middleware_set(
        self, timezone_activate, mock_get_by_user
    ):
        """test_timezone_middleware_set

        Returns:

        """
        # Arrange
        get_response = MagicMock()
        request = self.factory.post("core_main_set_timezone")
        request.user = create_mock_user("1")
        mock_get_by_user.return_value = UserPreferences(
            user_id=request.user.id, timezone="UTC"
        )
        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)

        # Act
        middleware = TimezoneMiddleware(get_response)
        middleware(request)

        # Assert
        self.assertTrue(timezone_activate.called)

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    @patch("django.utils.timezone.deactivate")
    def test_timezone_middleware_not_set(
        self, timezone_deactivate, mock_get_by_user
    ):
        """test_timezone_middleware_not_set

        Returns:

        """
        # Arrange
        get_response = MagicMock()
        request = self.factory.post("core_main_set_timezone")
        request.user = create_mock_user("1")
        mock_get_by_user.return_value = UserPreferences(
            user_id=request.user.id,
        )
        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)

        # Act
        middleware = TimezoneMiddleware(get_response)
        middleware(request)

        # Assert
        self.assertTrue(timezone_deactivate.called)

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    @patch("django.utils.timezone.deactivate")
    def test_timezone_middleware_user_preferences_not_found(
        self, timezone_deactivate, mock_get_by_user
    ):
        """test_timezone_middleware_not_set

        Returns:

        """
        # Arrange
        get_response = MagicMock()
        request = self.factory.post("core_main_set_timezone")
        request.user = create_mock_user("1")
        mock_get_by_user.side_effect = DoesNotExist("error")

        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)

        # Act
        middleware = TimezoneMiddleware(get_response)
        middleware(request)

        # Assert
        self.assertTrue(timezone_deactivate.called)
        self.assertEqual(
            request.session["django_timezone"], USER_TIMEZONE_NOT_SET
        )
