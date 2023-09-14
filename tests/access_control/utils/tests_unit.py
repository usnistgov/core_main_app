""" Unit tests for `core_main_app.access_control.utils`.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_main_app.access_control import utils as acl_utils
from core_main_app.permissions import rights
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCheckHasPerm(TestCase):
    """Unit tests for check_has_perm_function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_user = create_mock_user("1")

        self.mock_kwargs = {
            "user": self.mock_user,
            "permission_name": "mock_permission",
        }

    def test_superuser_does_not_call_has_perm(self):
        """test_superuser_does_not_call_has_perm"""
        super_user = create_mock_user("1", is_superuser=True)
        self.mock_kwargs["user"] = super_user

        acl_utils.check_has_perm(**self.mock_kwargs)
        super_user.has_perm.assert_not_called()

    @patch.object(acl_utils, "permissions_api")
    def test_permission_get_by_codename_is_called(self, mock_permissions_api):
        """test_permission_get_by_codename_is_called"""
        with self.assertRaises(AccessControlError):
            acl_utils.check_has_perm(**self.mock_kwargs)

        mock_permissions_api.get_by_codename.assert_called_with(
            self.mock_kwargs["permission_name"]
        )

    @patch.object(acl_utils, "logger")
    @patch.object(acl_utils, "permissions_api")
    def test_permission_get_by_codename_exception_raises_acl_error(
        self, mock_permissions_api, mock_logger
    ):
        """test_permission_get_by_codename_exception_raises_acl_error"""
        mock_permissions_api.get_by_codename.side_effect = Exception(
            "mock_get_by_codename_exception"
        )

        with self.assertRaises(AccessControlError):
            acl_utils.check_has_perm(**self.mock_kwargs)

        mock_logger.warning.assert_called()

    @patch.object(acl_utils, "group_api")
    @patch.object(acl_utils, "permissions_api")
    def test_get_by_name_and_permission_is_called(
        self, mock_permissions_api, mock_group_api
    ):
        """test_get_by_name_and_permission_is_called"""
        mock_permission_object = MagicMock()
        mock_permissions_api.get_by_codename.return_value = (
            mock_permission_object
        )
        self.mock_user.is_anonymous = True

        acl_utils.check_has_perm(**self.mock_kwargs)
        mock_group_api.get_by_name_and_permission.assert_called_with(
            name=rights.ANONYMOUS_GROUP,
            permission_codename=self.mock_kwargs["permission_name"],
        )

    @patch.object(acl_utils, "logger")
    @patch.object(acl_utils, "group_api")
    @patch.object(acl_utils, "permissions_api")
    def test_get_by_name_and_permission_exception_raises_acl_error(
        self, mock_permissions_api, mock_group_api, mock_logger
    ):
        """test_get_by_name_and_permission_exception_raises_acl_error"""
        mock_permission_object = MagicMock()
        mock_permissions_api.get_by_codename.return_value = (
            mock_permission_object
        )
        self.mock_user.is_anonymous = True
        mock_group_api.get_by_name_and_permission.side_effect = Exception(
            "mock_get_by_name_and_permission_exception"
        )

        with self.assertRaises(AccessControlError):
            acl_utils.check_has_perm(**self.mock_kwargs)

        mock_logger.warning.assert_called()

    @patch.object(acl_utils, "group_api")
    @patch.object(acl_utils, "permissions_api")
    def test_anonymous_cannot_access_raise_exception(
        self, mock_permissions_api, mock_group_api
    ):
        """test_anonymous_cannot_access_raise_exception"""
        mock_permission_object = MagicMock()
        mock_permissions_api.get_by_codename.return_value = (
            mock_permission_object
        )
        mock_group_api.get_by_name_and_permission.return_value = []
        self.mock_user.is_anonymous = True

        with self.assertRaises(AccessControlError):
            acl_utils.check_has_perm(**self.mock_kwargs)

    @patch.object(acl_utils, "group_api")
    @patch.object(acl_utils, "permissions_api")
    def test_anonymous_can_access_returns_none(
        self, mock_permissions_api, mock_group_api
    ):
        """test_anonymous_can_access_returns_none"""
        mock_permission_object = MagicMock()
        mock_permissions_api.get_by_codename.return_value = (
            mock_permission_object
        )
        mock_group_api.get_by_name_and_permission.return_value = [MagicMock()]
        self.mock_user.is_anonymous = True

        self.assertIsNone(acl_utils.check_has_perm(**self.mock_kwargs))

    @patch.object(acl_utils, "permissions_api")
    def test_user_has_perm_is_called(self, mock_permissions_api):
        """test_user_has_perm_is_called"""
        mock_permission_object = MagicMock()
        mock_permissions_api.get_by_codename.return_value = (
            mock_permission_object
        )

        with self.assertRaises(AccessControlError):
            acl_utils.check_has_perm(**self.mock_kwargs)

        self.mock_kwargs["user"].has_perm.assert_called_with(
            f"{mock_permission_object.content_type.app_label}."
            f"{mock_permission_object.codename}"
        )

    @patch.object(acl_utils, "logger")
    @patch.object(acl_utils, "permissions_api")
    def test_user_has_perm_exception_raises_acl_error(
        self, mock_permissions_api, mock_logger
    ):
        """test_user_has_perm_exception_raises_acl_error"""
        mock_permission_object = MagicMock()
        mock_permissions_api.get_by_codename.return_value = (
            mock_permission_object
        )
        self.mock_kwargs["user"].has_perm.side_effect = Exception(
            "mock_user_has_perm_exception"
        )

        with self.assertRaises(AccessControlError):
            acl_utils.check_has_perm(**self.mock_kwargs)

        mock_logger.warning.assert_called()

    @patch.object(acl_utils, "permissions_api")
    def test_registered_user_has_perm_false_raises_exception(
        self, mock_permissions_api  # noqa, pylint: disable=unused-argument
    ):
        """test_registered_user_has_perm_false_raises_exception"""
        self.mock_kwargs["user"].has_perm.return_value = False

        with self.assertRaises(AccessControlError):
            acl_utils.check_has_perm(**self.mock_kwargs)

    @patch.object(acl_utils, "permissions_api")
    def test_registered_user_has_perm_true_returns_none(
        self, mock_permissions_api  # noqa, pylint: disable=unused-argument
    ):
        """test_registered_user_has_perm_true_returns_none"""
        self.mock_kwargs["user"].has_perm.return_value = True

        self.assertIsNone(acl_utils.check_has_perm(**self.mock_kwargs))
