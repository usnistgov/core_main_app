""" Unit test for `views.user.views` package.
"""
from unittest.mock import patch, MagicMock

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, SimpleTestCase, override_settings

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.user_preferences.models import UserPreferences
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.views.user.views import (
    set_timezone,
    custom_login,
    custom_logout,
)


class TestSetTimezone(SimpleTestCase):
    """TestSetTimezone"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    def test_get_when_user_has_preferences_returns_form(
        self, mock_get_by_user
    ):
        """test_get_when_user_has_preferences_returns_form

        Returns:

        """
        # Arrange
        mock_get_by_user.return_value = UserPreferences(
            user_id="1", timezone="GMT"
        )
        request = self.factory.get("core_main_set_timezone")
        request.user = self.user1

        # Act
        response = set_timezone(request)

        # Assert
        self.assertTrue("form" in response.content.decode())
        self.assertTrue(
            '<option value="GMT" selected>GMT</option>'
            in response.content.decode()
        )

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    def test_get_returns_form(self, mock_get_by_user):
        """test_get_returns_form

        Returns:

        """
        # Arrange
        mock_get_by_user.return_value = UserPreferences(
            user_id="1", timezone="Africa/Casablanca"
        )
        request = self.factory.get("core_main_set_timezone")
        request.user = self.user1

        # Act
        response = set_timezone(request)

        # Assert
        self.assertTrue("form" in response.content.decode())
        self.assertTrue(
            '<option value="Africa/Casablanca" selected>Africa/Casablanca</option>'
            in response.content.decode()
        )

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    @patch("core_main_app.components.user_preferences.api.upsert")
    def test_post_update_redirects(self, mock_upsert, mock_get_by_user):
        """test_post_update_redirects

        Args:
            mock_get_by_user:
            mock_upsert:

        Returns:

        """
        mock_get_by_user.return_value = UserPreferences(
            user_id="1", timezone="GMT"
        )
        mock_upsert.return_value = UserPreferences(user_id="1", timezone="UTC")

        # Arrange
        request = self.factory.post("core_main_set_timezone")
        request.POST = {"timezone": "UTC"}
        request.user = self.user1
        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)

        # Act
        response = set_timezone(request)

        # Assert
        self.assertEqual(response.status_code, 302)

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    @patch("core_main_app.components.user_preferences.api.upsert")
    def test_post_new_redirects(self, mock_upsert, mock_get_by_user):
        """test_post_new_redirects

        Args:
            mock_get_by_user:
            mock_upsert:

        Returns:

        """
        mock_get_by_user.side_effect = DoesNotExist("error")
        mock_upsert.return_value = UserPreferences(user_id="1", timezone="UTC")

        # Arrange
        request = self.factory.post("core_main_set_timezone")
        request.POST = {"timezone": "UTC"}
        request.user = self.user1
        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)

        # Act
        response = set_timezone(request)

        # Assert
        self.assertEqual(response.status_code, 302)

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    def test_get_acl_error_returns_error(self, mock_get_by_user):
        # Arrange
        mock_get_by_user.side_effect = AccessControlError("error")
        request = self.factory.post("core_main_set_timezone")
        request.user = create_mock_user("1")

        # Act
        response = set_timezone(request)

        # Assert
        self.assertTrue("Access Forbidden" in response.content.decode())


class TestDefaultCustomLogin(SimpleTestCase):
    """TestDefaultCustomLogin"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.connected_user = create_mock_user(user_id="1")
        self.inactive_user = create_mock_user(user_id=None, is_active=False)

    @override_settings(INSTALLED_APPS=["core_main_app"])
    @patch("core_main_app.components.web_page_login.api.get")
    def test_get_returns_login_form_and_forget_password_button(
        self, mock_web_page_login_get
    ):
        """test_post_inactive_user_shows_form_with_error

        Returns:

        """
        # Arrange
        request = self.factory.get("core_main_app_login")
        request.user = self.anonymous_user
        mock_web_page_login_get.return_value = None

        # Act
        response = custom_login(request)

        # Assert
        self.assertTrue("form" in response.content.decode())
        self.assertTrue("Forgot password" in response.content.decode())

    @override_settings(INSTALLED_APPS=["core_main_app"])
    @patch("core_main_app.components.web_page_login.api.get")
    @patch("django.contrib.auth.authenticate")
    @patch("django.contrib.auth.login")
    def test_post_inactive_user_shows_form_with_error(
        self,
        mock_login,
        mock_authenticate,
        mock_web_page_login_get,
    ):
        """test_post_inactive_user_shows_form_with_error

        Returns:

        """
        # Arrange
        request = self.factory.post("core_main_app_login")
        request.method = "POST"
        request.POST = {
            "username": "user",
            "password": "pass",
            "next_page": None,
        }
        request.user = self.inactive_user
        mock_web_page_login_get.return_value = None
        mock_authenticate.return_value = self.inactive_user
        mock_login.return_value = None

        # Act
        response = custom_login(request)

        # Assert
        self.assertTrue("form" in response.content.decode())
        self.assertTrue(
            "Your username is not activated yet." in response.content.decode()
        )

    @override_settings(INSTALLED_APPS=["core_main_app"])
    @patch("core_main_app.components.web_page_login.api.get")
    @patch("django.contrib.auth.authenticate")
    @patch("django.contrib.auth.login")
    def test_post_active_user_redirects_to_page(
        self,
        mock_login,
        mock_authenticate,
        mock_web_page_login_get,
    ):
        """test_post_inactive_user_shows_form_with_error

        Returns:

        """
        # Arrange
        request = self.factory.post("core_main_app_login")
        request.method = "POST"
        request.POST = {
            "username": "user",
            "password": "pass",
            "next_page": None,
        }
        request.user = self.inactive_user
        mock_web_page_login_get.return_value = None
        mock_authenticate.return_value = self.connected_user
        mock_login.return_value = None

        # Act
        response = custom_login(request)

        # Assert
        self.assertTrue(response.status_code, 302)

    @override_settings(INSTALLED_APPS=["core_main_app"])
    @patch("core_main_app.components.web_page_login.api.get")
    @patch("django.contrib.auth.authenticate")
    @patch("django.contrib.auth.login")
    def test_post_with_error_renders_login_page_with_errors(
        self,
        mock_login,
        mock_authenticate,
        mock_web_page_login_get,
    ):
        """test_post_inactive_user_shows_form_with_error

        Returns:

        """
        # Arrange
        request = self.factory.post("core_main_app_login")
        request.method = "POST"
        request.POST = {
            "username": "user",
            "password": "pass",
            "next_page": None,
        }
        request.user = self.inactive_user
        mock_web_page_login_get.return_value = None
        mock_authenticate.return_value = self.connected_user
        mock_login.side_effect = Exception()

        # Act
        response = custom_login(request)

        # Assert
        self.assertTrue("form" in response.content.decode())
        self.assertTrue(
            "Invalid username and/or password." in response.content.decode()
        )


class TestCustomLogout(SimpleTestCase):
    """TestCustomLogout"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.connected_user = create_mock_user(user_id="1")

    @override_settings(INSTALLED_APPS=["core_main_app"])
    @patch("django.contrib.auth.logout")
    def test_logout_redirects(self, mock_logout):
        """test_logout_redirects

        Returns:

        """
        # Arrange
        request = self.factory.get("core_main_app_logout")
        request.user = self.connected_user
        mock_logout.return_value = None

        # Act
        response = custom_logout(request)

        # Assert
        self.assertTrue(response.status_code, 302)
