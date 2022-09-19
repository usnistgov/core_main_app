""" Unit Test Access Control
"""
from unittest.case import TestCase

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import ApiError
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_main_app.access_control import api as access_control_api


class TestAccessControlIsSuperuser(TestCase):
    """Test Access Control Is Superuser"""

    def setUp(self):
        """setUp"""
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.superuser = create_mock_user(user_id="1", is_superuser=True)

    def test_access_control_is_superuser_as_anonymous_raises_access_control_error(
        self,
    ):
        """test access control is superuser as anonymous raises access control error

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=self.anonymous_user)

        # Act # Assert
        with self.assertRaises(AccessControlError):
            access_control_api.is_superuser(
                mock_function, request=mock_request
            )

    def test_access_control_is_superuser_as_user_raises_access_control_error(
        self,
    ):
        """test access control is superuser as user raises access control error

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=self.user1)

        # Act # Assert
        with self.assertRaises(AccessControlError):
            access_control_api.is_superuser(
                mock_function, request=mock_request
            )

    def test_access_control_is_superuser_as_superuser_raises_api_error(self):
        """test access control is superuser as super raises api error

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=self.superuser)
        exception = ApiError("")

        # Act # Assert
        with self.assertRaises(ApiError):
            access_control_api.is_superuser(
                mock_function, exception, request=mock_request
            )

    def test_access_control_is_superuser_as_superuser_raises_access_control_error(
        self,
    ):
        """test access control is superuser as super raises  access control error

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=self.superuser)
        access_control_error = AccessControlError("")

        # Act # Assert
        with self.assertRaises(AccessControlError):
            access_control_api.is_superuser(
                mock_function, access_control_error, request=mock_request
            )

    def test_access_control_is_superuser_as_superuser_returns_function(self):
        """test access control is superuser as superuser returns function

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=self.superuser)

        # Act
        result = access_control_api.is_superuser(
            mock_function, request=mock_request
        )

        # Assert
        self.assertEqual(result, True)


def mock_function(exception=None, *args, **kwargs):
    """setUp

    Args:
        exception:
        args:
        kwargs:

    Returns:
    """
    if exception:
        raise exception
    return True
