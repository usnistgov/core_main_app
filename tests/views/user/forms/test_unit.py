""" Test forms.
"""
from unittest.case import TestCase
from unittest.mock import patch

from django.test import override_settings

from core_main_app.components.workspace.models import Workspace
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.views.user.forms import ChangeWorkspaceForm


class TestChangeWorkspaceForm(TestCase):
    """Test Change Workspace Form"""

    @override_settings(BOOTSTRAP_VERSION="4.6.2")
    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_change_workspace_form_bootstrap_v4(
        self, mock_get_all_workspaces_with_read_access_by_user, mock_user
    ):
        """test_change_workspace_form_bootstrap_v4

        Returns:

        """
        mock_get_all_workspaces_with_read_access_by_user.return_value = [
            Workspace(id=1)
        ]
        user = create_mock_user(user_id="1")
        user.username = "test"
        mock_user.return_value = user
        data = {"workspaces": list()}
        form = ChangeWorkspaceForm(data)
        self.assertEquals(
            form.fields["workspaces"].widget.attrs["class"], "form-control"
        )

    @override_settings(BOOTSTRAP_VERSION="5.1.3")
    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_change_workspace_form_bootstrap_v5(
        self, mock_get_all_workspaces_with_read_access_by_user, mock_user
    ):
        """test_change_workspace_form_bootstrap_v5

        Returns:

        """
        mock_get_all_workspaces_with_read_access_by_user.return_value = [
            Workspace(id=1)
        ]
        user = create_mock_user(user_id="1")
        user.username = "test"
        mock_user.return_value = user
        data = {"workspaces": list()}
        form = ChangeWorkspaceForm(data)
        self.assertEquals(
            form.fields["workspaces"].widget.attrs["class"], "form-select"
        )
