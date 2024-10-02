""" Allauth Adapter utils test class
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.utils.allauth.cdcs_adapter import CDCSAccountAdapter
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCDCSAccountAdapter(TestCase):
    """TestCDCSAccountAdapter"""

    @patch("core_website_app.components.account_request.api.insert")
    def test_save_user_returns_inactive_user(
        self, mock_account_request_api_insert
    ):
        """test_save_user_returns_inactive_user

        Returns:

        """
        mock_request = MagicMock()
        mock_user = create_mock_user("1")
        mock_form = MagicMock()

        cdcs_adapter = CDCSAccountAdapter(mock_request)
        saved_user = cdcs_adapter.save_user(mock_request, mock_user, mock_form)

        self.assertTrue(mock_account_request_api_insert.called)
        self.assertFalse(saved_user.is_active)
