""" Unit tests for `core_main_app.access_control.api`.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.access_control import api as access_control_api
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCanAnonymousAccessPublicData(TestCase):
    """Unit tests for `can_anonymous_access_public_data` function."""

    @patch.object(access_control_api, "check_anonymous_access")
    def test_check_anonymous_access_called(self, mock_check_anonymous_access):
        """test_check_anonymous_access_called"""
        user = create_mock_user("1")

        access_control_api.can_anonymous_access_public_data(
            MagicMock(), *[user]
        )

        mock_check_anonymous_access.assert_called_with(user)

    @patch.object(access_control_api, "check_anonymous_access")
    def test_returns_function(self, mock_check_anonymous_access):
        """test_returns_function"""
        func = MagicMock()
        user = create_mock_user("1")

        access_control_api.can_anonymous_access_public_data(func, *[user])

        func.assert_called()
