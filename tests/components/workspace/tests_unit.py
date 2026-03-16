"""Unit Test for Workspace API"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.workspace.access_control import (
    _check_is_owner_workspace,
)
from core_main_app.components.workspace.api import (
    can_user_read_workspace,
    can_user_write_workspace,
    get_all_by_owner,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCheckIsOwnerWorkspace(TestCase):
    """TestCheckIsOwnerWorkspace"""

    def test_check_is_owner_workspace_does_not_raise_if_same_id(self):
        """test_check_is_owner_workspace_does_not_raise_if_same_id"""
        mock_user = create_mock_user(1)
        mock_workspace = MagicMock()
        mock_workspace.owner = str(mock_user.id)
        _check_is_owner_workspace(mock_workspace, mock_user)

    def test_check_is_owner_workspace_raises_error_if_different_id(self):
        """test_check_is_owner_workspace_raises_error_if_different_id"""
        mock_user = create_mock_user(1)
        mock_workspace = MagicMock()
        mock_workspace.owner = "2"
        with self.assertRaises(AccessControlError):
            _check_is_owner_workspace(mock_workspace, mock_user)

    def test_check_is_owner_workspace_raises_error_if_different_id_none(self):
        """test_check_is_owner_workspace_raises_error_if_different_id_none"""
        mock_user = create_mock_user(1)
        mock_workspace = MagicMock()
        mock_workspace.owner = None
        with self.assertRaises(AccessControlError):
            _check_is_owner_workspace(mock_workspace, mock_user)

    def test_check_is_owner_workspace_raises_error_if_anonymous_and_workspace_owner_set(
        self,
    ):
        """test_check_is_owner_workspace_raises_error_if_anonymous_and_workspace_owner_set"""
        mock_user = create_mock_user(None, is_anonymous=True)
        mock_workspace = MagicMock()
        mock_workspace.owner = "1"
        with self.assertRaises(AccessControlError):
            _check_is_owner_workspace(mock_workspace, mock_user)

    def test_check_is_owner_workspace_raises_error_if_anonymous_and_workspace_owner_not_set(
        self,
    ):
        """test_check_is_owner_workspace_raises_error_if_anonymous_and_workspace_owner_not_set"""
        mock_user = create_mock_user(None, is_anonymous=True)
        mock_workspace = MagicMock()
        mock_workspace.owner = None
        with self.assertRaises(AccessControlError):
            _check_is_owner_workspace(mock_workspace, mock_user)

    def test_check_is_owner_workspace_raises_error_if_no_user_and_workspace_owner_set(
        self,
    ):
        """test_check_is_owner_workspace_raises_error_if_anonymous_and_workspace_owner_set"""
        mock_user = None
        mock_workspace = MagicMock()
        mock_workspace.owner = "1"
        with self.assertRaises(AccessControlError):
            _check_is_owner_workspace(mock_workspace, mock_user)

    def test_check_is_owner_workspace_raises_error_if_no_user_and_workspace_owner_not_set(
        self,
    ):
        """test_check_is_owner_workspace_raises_error_if_no_user_and_workspace_owner_not_set"""
        mock_user = None
        mock_workspace = MagicMock()
        mock_workspace.owner = None
        with self.assertRaises(AccessControlError):
            _check_is_owner_workspace(mock_workspace, mock_user)


class TestCanUserReadWorkspace(TestCase):

    @patch("core_main_app.components.workspace.api.permission_api")
    def test_can_user_read_workspace_returns_true_if_same_id_no_perm(
        self, mock_permission_api
    ):
        mock_permission_api.get_permission_label.return_value = "label"
        mock_user = create_mock_user(1)
        mock_user.has_perm.return_value = False
        mock_workspace = MagicMock()
        mock_workspace.owner = str(mock_user.id)
        mock_workspace.is_public = False
        can_read = can_user_read_workspace(mock_workspace, mock_user)
        self.assertTrue(mock_permission_api.get_permission_label.called)
        self.assertTrue(can_read)

    @patch("core_main_app.components.workspace.api.permission_api")
    def test_can_user_read_workspace_no_owner_returns_true_if_no_id_no_perm(
        self, mock_permission_api
    ):
        mock_permission_api.get_permission_label.return_value = "label"
        mock_user = create_mock_user(None)
        mock_user.has_perm.return_value = False
        mock_workspace = MagicMock()
        mock_workspace.owner = None
        mock_workspace.is_public = False
        can_read = can_user_read_workspace(mock_workspace, mock_user)
        self.assertTrue(mock_permission_api.get_permission_label.called)
        self.assertFalse(can_read)


class TestCanUserWriteWorkspace(TestCase):

    @patch("core_main_app.components.workspace.api.permission_api")
    def test_can_user_write_workspace_returns_true_if_same_id_no_perm(
        self, mock_permission_api
    ):
        mock_permission_api.get_permission_label.return_value = "label"
        mock_user = create_mock_user(1)
        mock_user.has_perm.return_value = False
        mock_workspace = MagicMock()
        mock_workspace.owner = str(mock_user.id)
        can_write = can_user_write_workspace(mock_workspace, mock_user)
        self.assertTrue(mock_permission_api.get_permission_label.called)
        self.assertTrue(can_write)

    @patch("core_main_app.components.workspace.api.permission_api")
    def test_can_user_write_workspace_no_owner_returns_true_if_no_id_no_perm(
        self, mock_permission_api
    ):
        mock_permission_api.get_permission_label.return_value = "label"
        mock_user = create_mock_user(None)
        mock_user.has_perm.return_value = False
        mock_workspace = MagicMock()
        mock_workspace.owner = None
        can_write = can_user_write_workspace(mock_workspace, mock_user)
        self.assertTrue(mock_permission_api.get_permission_label.called)
        self.assertFalse(can_write)


class TestGetAllByOwner(TestCase):

    @patch("core_main_app.components.workspace.api.Workspace")
    def test_get_all_by_owner_no_user_returns_none_qs(self, mock_workspace):
        mock_user = create_mock_user(None, is_anonymous=True)
        get_all_by_owner(mock_user)
        self.assertTrue(mock_workspace.objects.none.called)
        self.assertFalse(mock_workspace.get_all_by_owner.called)

    @patch("core_main_app.components.workspace.api.Workspace")
    def test_get_all_by_owner_with_user_calls_get_all_by_owner(
        self, mock_workspace
    ):
        mock_user = create_mock_user("1")
        get_all_by_owner(mock_user)
        self.assertFalse(mock_workspace.objects.none.called)
        self.assertTrue(mock_workspace.get_all_by_owner.called)
