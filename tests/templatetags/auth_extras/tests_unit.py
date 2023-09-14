""" Unit tests for `core_main_app.templatetags.auth_extras`
"""
from unittest import TestCase
from unittest.mock import patch

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.templatetags import auth_extras
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestHasPerm(TestCase):
    """Unit tests for `has_perm` template tag."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_user = create_mock_user("1")
        self.mock_kwargs = {
            "user": self.mock_user,
            "permission": "core_pkg.perm_name",
        }

    @patch.object(auth_extras, "check_has_perm")
    def test_check_has_perm_called(self, mock_check_has_perm):
        """test_check_has_perm_called"""
        auth_extras.has_perm(**self.mock_kwargs)

        mock_check_has_perm.assert_called_with(
            self.mock_user, self.mock_kwargs["permission"].split(".")[1]
        )

    @patch.object(auth_extras, "check_has_perm")
    def test_check_has_perm_success_returns_true(self, mock_check_has_perm):
        """test_check_has_perm_called"""
        mock_check_has_perm.return_value = None
        self.assertTrue(auth_extras.has_perm(**self.mock_kwargs))

    @patch.object(auth_extras, "check_has_perm")
    def test_acl_error_returns_false(self, mock_check_has_perm):
        """test_check_has_perm_called"""
        mock_check_has_perm.side_effect = AccessControlError(
            "mock_check_has_perm_acl_error"
        )
        self.assertFalse(auth_extras.has_perm(**self.mock_kwargs))
