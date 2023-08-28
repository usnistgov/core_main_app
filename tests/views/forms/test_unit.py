""" Test forms.
"""
from unittest.case import TestCase
from unittest.mock import patch

from django.test import override_settings

from core_main_app.components.workspace.models import Workspace
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.views.admin.forms import (
    TemplateXsltRenderingForm,
    UploadTemplateForm,
)
from core_main_app.views.user.forms import ChangeWorkspaceForm


class TestTemplateXsltRenderingForm(TestCase):
    """Test Template Xslt Rendering Form"""

    @override_settings(BOOTSTRAP_VERSION="4.6.2")
    def test_template_xslt_rendering_form_bootstrap_v4(self):
        """test_template_xslt_rendering_form_bootstrap_v4

        Returns:

        """
        data = {}
        form = TemplateXsltRenderingForm(data)
        self.assertEquals(
            form.fields["default_detail_xslt"].widget.attrs["class"],
            "form-control",
        )
        self.assertEquals(
            form.fields["list_xslt"].widget.attrs["class"], "form-control"
        )

    @override_settings(BOOTSTRAP_VERSION="5.1.3")
    def test_template_xslt_rendering_form_bootstrap_v5(self):
        """test_template_xslt_rendering_form_bootstrap_v5

        Returns:

        """
        data = {}
        form = TemplateXsltRenderingForm(data)
        self.assertEquals(
            form.fields["default_detail_xslt"].widget.attrs["class"],
            "form-select",
        )
        self.assertEquals(
            form.fields["list_xslt"].widget.attrs["class"], "form-select"
        )


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


class TestUploadTemplateForm(TestCase):
    def test_upload_form_sets_extension_validators(
        self,
    ):
        """test_upload_form_sets_extension_validators

        Returns:

        """
        form = UploadTemplateForm()
        self.assertEquals(
            form.fields["upload_file"].validators[0].valid_extensions,
            ".json,.xsd",
        )
