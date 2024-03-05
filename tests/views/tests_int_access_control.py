""" Test access to views
"""
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import QueryDict
from django.test import RequestFactory

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import ModelError
from core_main_app.components.blob import api as blob_api
from core_main_app.components.data import api as data_api
from core_main_app.settings import MAX_DOCUMENT_EDITING_SIZE
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_main_app.views.common.views import (
    ViewData,
    EditWorkspaceRights,
    TemplateXSLRenderingView,
    DataXMLEditor,
    TemplateXSDEditor,
    TemplateJSONEditor,
    AbstractEditorView,
    ViewBlob,
    ManageBlobMetadata,
    DataJSONEditor,
)
from core_main_app.views.user.ajax import (
    AssignView,
    change_data_display,
    LoadFormChangeWorkspace,
    load_add_user_form,
    add_user_right_to_workspace,
    switch_right,
    remove_user_or_group_rights,
    load_add_group_form,
    add_group_right_to_workspace,
    UploadFile,
    RemoveMetadataFromBlob,
    AddMetadataToBlob,
    LoadBlobMetadataForm,
)
from core_main_app.views.user.views import manage_template_versions
from tests.components.data.fixtures.fixtures import (
    AccessControlBlobWithMetadataFixture,
)
from tests.test_settings import LOGIN_URL
from tests.views.fixtures import AccessControlDataFixture, JSONDataFixtures


class TestViewData(IntegrationBaseTestCase):
    """TestViewData"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_a_user_can_access_a_data_if_owner(self):
        """test_a_user_can_access_a_data_if_owner

        Returns:

        """
        request = self.factory.get("core_main_app_data_detail")
        request.user = self.user1
        request.GET = {"id": str(self.fixture.data_1.id)}
        response = ViewData.as_view()(request)
        self.assertTrue(self.fixture.data_1.title in response.content.decode())

    def test_an_anonymous_user_can_not_access_a_data_that_is_not_in_a_workspace(
        self,
    ):
        """test_an_anonymous_user_can_not_access_a_data_that_is_not_in_a_workspace

        Returns:

        """
        request = self.factory.get("core_main_app_data_detail")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.data_1.id)}
        response = ViewData.as_view()(request)
        self.assertTrue(
            self.fixture.data_1.title not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())

    def test_an_anonymous_user_can_not_access_a_data_that_is_in_a_private_workspace(
        self,
    ):
        """test_an_anonymous_user_can_not_access_a_data_that_is_in_a_private_workspace

        Returns:

        """
        request = self.factory.get("core_main_app_data_detail")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.data_1.id)}
        response = ViewData.as_view()(request)
        self.assertTrue(
            self.fixture.data_1.title not in response.content.decode()
        )
        self.assertTrue("Error" in response.content.decode())

    def test_an_anonymous_user_can_not_access_a_data_that_is_in_a_public_workspace_and_access_setting_is_false(
        self,
    ):
        """test_an_anonymous_user_can_not_access_a_data_that_is_in_a_public_workspace_and_access_setting_is_false

        Returns:

        """
        request = self.factory.get("core_main_app_data_detail")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.data_public_workspace.id)}
        response = ViewData.as_view()(request)
        self.assertTrue(
            self.fixture.data_public_workspace.title
            not in response.content.decode()
        )
        self.assertTrue("Error" in response.content.decode())


class TestManageTemplateVersions(IntegrationBaseTestCase):
    """TestManageTemplateVersions"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_manage_template_versions(self):
        """test_an_anonymous_user_can_not_manage_template_versions

        Returns:

        """
        request = self.factory.get("core_main_app_manage_template_versions")
        request.user = self.anonymous
        response = manage_template_versions(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestTemplateXSLRenderingView(IntegrationBaseTestCase):
    """TestTemplateXSLRenderingView"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_manage_template_versions(self):
        """test_an_anonymous_user_can_not_manage_template_versions

        Returns:

        """
        request = self.factory.get("core_main_app_template_xslt")
        request.user = self.anonymous
        response = TemplateXSLRenderingView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestAssignDataView(IntegrationBaseTestCase):
    """TestAssignDataView"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_a_user_can_assign_a_data_if_owner(self):
        """test_a_user_can_assign_a_data_if_owner

        Returns:

        """
        data = {
            "document_id[]": [str(self.fixture.data_1.id)],
            "workspace_id[]": [str(self.fixture.workspace_2.id)],
        }
        request = self.factory.post("core_main_assign_data_workspace", data)
        request.user = self.user1
        response = AssignView.as_view(api=data_api)(request)
        self.assertEqual(response.status_code, 200)

    def test_an_anonymous_user_can_not_assign_a_user_data(self):
        """test_an_anonymous_user_can_not_assign_a_user_data

        Returns:

        """
        data = {
            "document_id[]": [str(self.fixture.data_1.id)],
            "workspace_id[]": [str(self.fixture.workspace_2.id)],
        }
        request = self.factory.post("core_main_assign_data_workspace", data)
        request.user = self.anonymous
        response = AssignView.as_view(api=data_api)(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_an_anonymous_user_can_not_assign_a_workspace_data(self):
        """test_an_anonymous_user_can_not_assign_a_workspace_data

        Returns:

        """
        data = {
            "document_id[]": [str(self.fixture.data_workspace_1.id)],
            "workspace_id[]": [str(self.fixture.workspace_2.id)],
        }
        request = self.factory.post("core_main_assign_data_workspace", data)
        request.user = self.anonymous
        response = AssignView.as_view(api=data_api)(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_an_anonymous_user_can_not_assign_a_public_workspace_data(self):
        """test_an_anonymous_user_can_not_assign_a_public_workspace_data

        Returns:

        """
        data = {
            "document_id[]": [str(self.fixture.data_public_workspace.id)],
            "workspace_id[]": [str(self.fixture.workspace_2.id)],
        }
        request = self.factory.post("core_main_assign_data_workspace", data)
        request.user = self.anonymous
        response = AssignView.as_view(api=data_api)(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestAssignBlobView(IntegrationBaseTestCase):
    """TestAssignBlobView"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_a_user_can_assign_a_blob_if_owner(self):
        """test_a_user_can_assign_a_blob_if_owner

        Returns:

        """
        data = {
            "document_id[]": [str(self.fixture.blob_1.id)],
            "workspace_id[]": [str(self.fixture.workspace_2.id)],
        }
        request = self.factory.post("core_main_assign_blob_workspace", data)
        request.user = self.user1
        response = AssignView.as_view(api=blob_api)(request)
        self.assertEqual(response.status_code, 200)

    def test_an_anonymous_user_can_not_assign_a_user_blob(self):
        """test_an_anonymous_user_can_not_assign_a_user_blob

        Returns:

        """
        data = {
            "document_id[]": [str(self.fixture.blob_1.id)],
            "workspace_id[]": [str(self.fixture.workspace_2.id)],
        }
        request = self.factory.post("core_main_assign_blob_workspace", data)
        request.user = self.anonymous
        response = AssignView.as_view(api=blob_api)(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_an_anonymous_user_can_not_assign_a_workspace_blob(self):
        """test_an_anonymous_user_can_not_assign_a_workspace_blob

        Returns:

        """
        data = {
            "document_id[]": [str(self.fixture.blob_workspace_1.id)],
            "workspace_id[]": [str(self.fixture.workspace_2.id)],
        }
        request = self.factory.post("core_main_assign_blob_workspace", data)
        request.user = self.anonymous
        response = AssignView.as_view(api=blob_api)(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))

    def test_an_anonymous_user_can_not_assign_a_public_workspace_blob(self):
        """test_an_anonymous_user_can_not_assign_a_public_workspace_blob

        Returns:

        """
        data = {
            "document_id[]": [str(self.fixture.blob_public_workspace.id)],
            "workspace_id[]": [str(self.fixture.workspace_2.id)],
        }
        request = self.factory.post("core_main_assign_blob_workspace", data)
        request.user = self.anonymous
        response = AssignView.as_view(api=blob_api)(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestChangeDataDisplayView(IntegrationBaseTestCase):
    """TestChangeDataDisplayView"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_a_user_can_change_data_display_if_owner(self):
        """test_a_user_can_change_data_display_if_owner

        Returns:

        """
        data = {"xslt_id": "id", "data_id": str(self.fixture.data_1.id)}
        request = self.factory.post("core_main_add_change_data_display", data)
        request.user = self.user1
        response = change_data_display(request)
        self.assertEqual(response.status_code, 200)

    def test_change_data_display_returns_http_200(self):
        """test_change_data_display_returns_http_200

        Returns:

        """
        data = {
            "xslt_id": "1",
            "template_id": str(self.fixture.data_1.template.id),
            "content": "<tag></tag>",
        }
        request = self.factory.post("core_main_add_change_data_display", data)
        request.user = self.user1
        response = change_data_display(request)
        self.assertEqual(response.status_code, 200)

    def test_change_data_display_returns_error_when_template_id_is_missing(
        self,
    ):
        """test_change_data_display_returns_error_when_template_id_is_missing

        Returns:

        """
        data = {
            "xslt_id": "1",
            "content": "<tag></tag>",
        }
        request = self.factory.post("core_main_add_change_data_display", data)
        request.user = self.user1
        response = change_data_display(request)
        self.assertEqual(response.status_code, 400)

    def test_an_anonymous_user_can_not_assign_a_user_data(self):
        """test_an_anonymous_user_can_not_assign_a_user_data

        Returns:

        """
        data = {"xslt_id": "id", "data_id": str(self.fixture.data_1.id)}
        request = self.factory.post("core_main_add_change_data_display", data)
        request.user = self.anonymous
        response = change_data_display(request)
        self.assertEqual(response.status_code, 403)

    def test_an_anonymous_user_can_not_assign_a_workspace_data(self):
        """test_an_anonymous_user_can_not_assign_a_workspace_data

        Returns:

        """
        data = {
            "xslt_id": "id",
            "data_id": str(self.fixture.data_workspace_1.id),
        }
        request = self.factory.post("core_main_add_change_data_display", data)
        request.user = self.anonymous
        response = change_data_display(request)
        self.assertEqual(response.status_code, 403)

    def test_an_anonymous_user_can_not_assign_a_public_workspace_data(self):
        """test_an_anonymous_user_can_not_assign_a_public_workspace_data

        Returns:

        """
        data = {
            "xslt_id": "id",
            "data_id": str(self.fixture.data_public_workspace.id),
        }
        request = self.factory.post("core_main_add_change_data_display", data)
        request.user = self.anonymous
        response = change_data_display(request)
        self.assertEqual(response.status_code, 403)


class TestEditRights(IntegrationBaseTestCase):
    """TestEditRights"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_edit_rights_workspace(self):
        """test_an_anonymous_user_can_not_edit_rights_workspace

        Returns:

        """
        request = self.factory.post("core_main_edit_rights_workspace")
        request.user = self.anonymous
        response = EditWorkspaceRights.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestLoadFormChangeWorkspace(IntegrationBaseTestCase):
    """TestLoadFormChangeWorkspace"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_load_form_change_workspace(self):
        """test_an_anonymous_user_can_not_load_form_change_workspace

        Returns:

        """
        data = {"administration": "True"}
        request = self.factory.post("core_main_change_workspace", data)
        request.user = self.anonymous
        response = LoadFormChangeWorkspace.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestLoadAddUserForm(IntegrationBaseTestCase):
    """TestLoadAddUserForm"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_load_add_user_form(self):
        """test_an_anonymous_user_can_not_load_add_user_form

        Returns:

        """
        request = self.factory.post("core_main_edit_rights_users_form")
        request.user = self.anonymous
        response = load_add_user_form(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestAddUserToWorkspace(IntegrationBaseTestCase):
    """TestAddUserToWorkspace"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_add_user_to_workspace(self):
        """test_an_anonymous_user_can_not_add_user_to_workspace

        Returns:

        """
        request = self.factory.post("core_main_add_user_right_to_workspace")
        request.user = self.anonymous
        response = add_user_right_to_workspace(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestSwitchRight(IntegrationBaseTestCase):
    """TestSwitchRight"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_switch_right(self):
        """test_an_anonymous_user_can_not_switch_right

        Returns:

        """
        request = self.factory.post("core_main_switch_right")
        request.user = self.anonymous
        response = switch_right(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestRemoveRights(IntegrationBaseTestCase):
    """TestRemoveRights"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_remove_rights(self):
        """test_an_anonymous_user_can_not_remove_rights

        Returns:

        """
        request = self.factory.post("core_main_remove_rights")
        request.user = self.anonymous
        response = remove_user_or_group_rights(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestAddGroupForm(IntegrationBaseTestCase):
    """TestAddGroupForm"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_add_group_form(self):
        """test_an_anonymous_user_can_not_add_group_form

        Returns:

        """
        request = self.factory.post("core_main_edit_rights_groups_form")
        request.user = self.anonymous
        response = load_add_group_form(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestAddGroupRightToWorkspace(IntegrationBaseTestCase):
    """TestAddGroupRightToWorkspace"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_add_group_right_to_workspace(self):
        """test_an_anonymous_user_can_not_add_group_right_to_workspace

        Returns:

        """
        request = self.factory.post("core_main_add_group_right_to_workspace")
        request.user = self.anonymous
        response = add_group_right_to_workspace(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(LOGIN_URL))


class TestAbstractTextEditorView(IntegrationBaseTestCase):
    """Test Abstract Text Editor View"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.request = create_mock_request(create_mock_user("1"))

    def test_format_raises_not_implemented_error(self):
        """test_format_raises_not_implemented_error

        Returns:

        """
        # Assert
        with self.assertRaises(NotImplementedError):
            AbstractEditorView.format(self)

    def test_validate_raises_not_implemented_error(self):
        """test_validate_raises_not_implemented_error

        Returns:

        """
        # Assert
        with self.assertRaises(NotImplementedError):
            AbstractEditorView.validate(self)

    def test_save_raises_not_implemented_error(self):
        """test_save_raises_not_implemented_error

        Returns:

        """
        # Assert
        with self.assertRaises(NotImplementedError):
            AbstractEditorView.save(self)

    def test_generate_raises_not_implemented_error(self):
        """test_generate_raises_not_implemented_error

        Returns:

        """
        # Assert
        with self.assertRaises(NotImplementedError):
            AbstractEditorView.generate(self)

    def test_get_object_raises_not_implemented_error(self):
        """test_get_object_raises_not_implemented_error

        Returns:

        """
        # Assert
        with self.assertRaises(NotImplementedError):
            AbstractEditorView._get_object(self, self.request)

    def test_check_permission_raises_not_implemented_error(self):
        """test_check_permission_raises_not_implemented_error

        Returns:

        """
        # Assert
        with self.assertRaises(NotImplementedError):
            AbstractEditorView._check_permission(self, None, self.request)

    def test_prepare_context_raises_not_implemented_error(self):
        """test_prepare_context_raises_not_implemented_error

        Returns:

        """
        # Assert
        with self.assertRaises(NotImplementedError):
            AbstractEditorView._prepare_context(self, None)

    def test_check_size_raises_not_implemented_error(self):
        """test_check_size_raises_not_implemented_error

        Returns:

        """
        # Assert
        with self.assertRaises(NotImplementedError):
            AbstractEditorView._check_size(self, None)

    def test_get_assets_raises_not_implemented_error(self):
        """test_get_assets_raises_not_implemented_error

        Returns:

        """
        # Act
        assets = {
            "js": [
                {
                    "path": "core_main_app/user/js/text_editor/text_editor.js",
                    "is_raw": True,
                },
            ],
            "css": [
                "core_main_app/user/css/text-editor.css",
            ],
        }
        # Assert
        self.assertEqual(AbstractEditorView._get_assets(self), assets)

    @patch("core_main_app.views.common.views.main_settings")
    def test_get_assets_as_monaco_editor_raises_not_implemented_error(
        self, mock_settings
    ):
        """test_get_assets_as_monaco_editor_raises_not_implemented_error

        Returns:

        """
        mock_settings.TEXT_EDITOR_LIBRARY = "Monaco"
        # Act
        assets = {
            "js": [
                {
                    "path": "core_main_app/user/js/text_editor/text_editor.js",
                    "is_raw": True,
                },
                {
                    "path": "core_main_app/user/js/text_editor/monaco-editor-loader.js",
                    "is_raw": True,
                },
                {
                    "path": "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.46.0/min/vs/loader.min.js",
                    "integrity": "sha512-ZG31AN9z/CQD1YDDAK4RUAvogwbJHv6bHrumrnMLzdCrVu4HeAqrUX7Jsal/cbUwXGfaMUNmQU04tQ8XXl5Znw==",
                    "is_external": True,
                    "is_raw": False,
                },
                {
                    "path": "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.46.0/min/vs/editor/editor.main.min.js",
                    "integrity": "sha512-AnszY619AdeYxGzR/u1bSnYCRmnGHrHLpOkc0qolt12NuhUJI4Cw+dRK0eiRChNxvY+C84xDE0HPPGdr3bCTZQ==",
                    "is_external": True,
                    "is_raw": False,
                },
                {
                    "path": "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.46.0/min/vs/editor/editor.main.nls.min.js",
                    "integrity": "sha512-E3GzU1Yj2NxL325SuAMqGvDn0W9+xr3WSkwEacvKo5Qh3wv60JToJUcIAUYrgtiF5tlwU2pztakxsp2UnHhbKA==",
                    "is_external": True,
                    "is_raw": False,
                },
            ],
            "css": [
                "core_main_app/user/css/text-editor.css",
            ],
            "external_css": [
                {
                    "path": "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.46.0/min/vs/editor/editor.main.min.css",
                    "integrity": "sha512-Q/ZIaWsdJBTBAkGTDqXN6AhYSD7+QEa+ccWJLsFTbayZWiv+Vi/BUGfm8E/4k/AV9Wvpci22/QSl56214Mv5NQ==",
                    "extra_args": {"data-name": "vs/editor/editor.main"},
                }
            ],
        }
        # Assert
        self.assertEqual(AbstractEditorView._get_assets(self), assets)

    def test_get_modals_raises_not_implemented_error(self):
        """test_get_modals_raises_not_implemented_error

        Returns:

        """

        # Act # Assert
        self.assertEqual(AbstractEditorView._get_modals(self), [])

    def test_get_context_raises_not_implemented_error(self):
        """test_get_context_raises_not_implemented_error

        Returns:

        """
        id = "0"
        name = "test"
        type_content = "None"
        content = "content"
        context = AbstractEditorView._get_context(
            self, id, name, type_content, content
        )
        # Assert
        self.assertEqual(context["name"], name)
        self.assertEqual(context["document_id"], id)
        self.assertEqual(context["content"], content)
        self.assertEqual(context["type"], type_content)


class TestDataXMLEditorView(IntegrationBaseTestCase):
    """Test Post Data Content Editor View"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_prepare_context_returns_context(self):
        """test_prepare_context_returns_context

        Returns:

        """
        request = self.factory.get("core_main_app_xml_text_editor_view")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.data_1.id)}
        data_editor = DataXMLEditor()
        data_editor.request = request
        context = data_editor._prepare_context(self.fixture.data_1)
        self.assertEqual(context["page_title"], "XML Text Editor")
        self.assertEqual(context["name"], self.fixture.data_1.title)
        self.assertEqual(context["type"], "XML")
        self.assertEqual(context["document_id"], self.fixture.data_1.id)
        self.assertEqual(context["document_name"], "Data")
        self.assertEqual(
            context["template_id"], self.fixture.data_1.template.id
        )

    def test_user_can_not_access_to_data_without_id(self):
        """test_user_can_not_access_to_data_without_id

        Returns:

        """
        request = self.factory.get("core_main_app_xml_text_editor_view")
        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertTrue("Error 400" in response.content.decode())

    def test_anonymous_user_can_not_access_to_data(self):
        """test_anonymous_user_can_not_access_to_data

        Returns:

        """
        request = self.factory.get("core_main_app_xml_text_editor_view")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.data_1.id)}
        response = DataXMLEditor.as_view()(request)
        self.assertTrue(
            self.fixture.data_1.title not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())

    def test_user_can_not_access_to_data_if_not_found(self):
        """test_user_can_not_access_a_data_if_not_found

        Returns:

        """
        request = self.factory.get("core_main_app_xml_text_editor_view")
        request.GET = {"id": "-1"}
        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertTrue("Error 404" in response.content.decode())

    def test_user_can_access_to_data_if_owner(self):
        """test_user_can_access_a_data_if_owner

        Returns:

        """
        request = self.factory.get("core_main_app_xml_text_editor_view")
        request.GET = {"id": str(self.fixture.data_1.id)}
        request.user = self.user1
        response = DataXMLEditor.as_view()(
            request,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_format_xml_content(self):
        """test_user_can_format_xml_content

        Returns:

        """
        data = {
            "content": "<root><element>value2</element></root>",
            "action": "format",
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)

        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_validate_xml_content(self):
        """test_user_can_validate_xml_content

        Returns:

        """
        data = {
            "content": "<root></root>",
            "action": "validate",
            "template_id": str(self.fixture.data_1.template.id),
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)

        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_validate_bad_xml_content_returns_error(self):
        """test_user_validate_xml_content_returns_error

        Returns:

        """
        data = {
            "content": "<tag></tag>",
            "action": "validate",
            "template_id": str(self.fixture.data_1.template.id),
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)
        request.user = self.user1

        response = DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_validate_empty_content_returns_error(self):
        """test_user_validate_empty_content_returns_error

        Returns:

        """
        data = {
            "content": "",
            "action": "validate",
            "template_id": str(self.fixture.data_1.template.id),
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)

        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_validate_xml_content_returns_error(self):
        """test_user_validate_xml_content_returns_error

        Returns:

        """
        data = {
            "content": "<root></root>",
            "action": "validate",
            "template_id": "",
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)
        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_can_save_xml_content(self):
        """test_user_can_save_xml_content

        Returns:

        """
        data = {
            "content": "<root></root>",
            "action": "save",
            "document_id": str(self.fixture.data_1.id),
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_save_xml_content_returns_acl_error(self):
        """test_user_save_xml_content_returns_acl_error

        Returns:

        """
        data = {
            "content": "<root></root>",
            "action": "save",
            "document_id": str(self.fixture.data_1.id),
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)
        request.user = self.anonymous
        response = DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_user_save_xml_content_returns_dne_error(self):
        """test_user_save_xml_content_returns_dne_error

        Returns:

        """
        data = {
            "content": "<root></root>",
            "action": "save",
            "document_id": "-1",
            "id": "-1",
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)
        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_save_xml_content_returns_error(self):
        """test_user_save_xml_content_returns_error

        Returns:

        """
        data = {
            "action": "save",
            "document_id": "-1",
            "id": "-1",
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)
        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    @patch("core_main_app.utils.file.get_byte_size_from_string")
    def test_xml_content_too_big_returns_error(self, mock_get_byte_size):
        """test_user_save_xml_content_returns_error

        Returns:

        """
        mock_get_byte_size.return_value = MAX_DOCUMENT_EDITING_SIZE + 1
        request = self.factory.get("core_main_app_xml_text_editor_view")
        request.GET = {"id": str(self.fixture.data_1.id)}
        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertTrue(
            "MAX_DOCUMENT_EDITING_SIZE" in response.content.decode()
        )


class TestXSDTextEditorView(IntegrationBaseTestCase):
    """Test Post XSD Text Editor View"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    def test_anonymous_user_can_not_access_template_content(self):
        """test_anonymous_user_can_not_access_template_content

        Returns:

        """
        request = self.factory.get("core_main_app_xsd_text_editor_view")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.template.id)}
        response = TemplateXSDEditor.as_view()(request)

        self.assertTrue("Error 403" in response.content.decode())

    def test_user_can_not_access_template_if_not_found(self):
        """test_user_can_not_access_template_if_not_found

        Returns:

        """
        request = self.factory.get("core_main_app_xsd_text_editor_view")
        request.user = self.user1
        request.GET = {"id": "-1"}
        response = TemplateXSDEditor.as_view()(request)
        self.assertTrue("Error 404" in response.content.decode())

    def test_user_can_access_template(self):
        """test_user_can_access_template

        Returns:

        """
        request = self.factory.get("core_main_app_xsd_text_editor_view")
        request.user = self.user1
        request.GET = {"id": str(self.fixture.template.id)}
        response = TemplateXSDEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_format_xsd_content(self):
        """test_user_can_format_xsd_content

        Returns:

        """
        data = {
            "content": self.fixture.template.content,
            "action": "format",
            "id": str(self.fixture.template.id),
        }
        request = self.factory.post("core_main_app_xsd_text_editor_view", data)

        request.user = self.user1
        response = TemplateXSDEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_validate_xsd_content(self):
        """test_user_can_validate_xsd_content

        Returns:

        """
        data = {
            "content": self.fixture.template.content,
            "action": "validate",
            "template_id": str(self.fixture.template.id),
            "id": str(self.fixture.template.id),
        }
        request = self.factory.post("core_main_app_xsd_text_editor_view", data)
        request.user = self.user1
        response = TemplateXSDEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_validate_empty_xsd_content_returns_error(self):
        """test_user_validate_empty_xsd_content_returns_error

        Returns:

        """
        data = {
            "content": "",
            "action": "validate",
            "template_id": str(self.fixture.template.id),
            "id": str(self.fixture.template.id),
        }
        request = self.factory.post("core_main_app_xsd_text_editor_view", data)
        request.user = self.user1
        response = TemplateXSDEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_validate_bad_xsd_content_returns_error(self):
        """test_user_validate_bad_xsd_content_returns_error

        Returns:

        """
        xsd = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element nam="root"></xs:element></xs:schema>'
        )
        data = {
            "content": xsd,
            "action": "validate",
            "template_id": str(self.fixture.template.id),
            "id": str(self.fixture.template.id),
        }
        request = self.factory.post("core_main_app_xsd_text_editor_view", data)
        request.user = self.user1
        response = TemplateXSDEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_can_save_xsd_content(self):
        """test_user_can_save_xsd_content

        Returns:

        """
        data = {
            "content": self.fixture.template.content,
            "action": "save",
            "id": str(self.fixture.template.id),
            "document_id": str(self.fixture.template.id),
        }
        request = self.factory.post("core_main_app_xsd_text_editor_view", data)
        request.user = self.user1
        response = TemplateXSDEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_save_xsd_content_returns_acl_error(self):
        """test_user_save_xsd_content_returns_acl_error

        Returns:

        """
        data = {
            "content": self.fixture.template.content,
            "action": "save",
            "id": str(self.fixture.template.id),
            "document_id": str(self.fixture.template.id),
        }
        request = self.factory.post("core_main_app_xsd_text_editor_view", data)
        request.user = self.anonymous
        response = TemplateXSDEditor.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_user_save_xml_content_returns_dne_error(self):
        """test_user_save_xsd_content_returns_dne_error

        Returns:

        """
        data = {
            "content": self.fixture.template.content,
            "action": "save",
            "id": "-1",
            "document_id": "-1",
        }
        request = self.factory.post("core_main_app_xsd_text_editor_view", data)
        request.user = self.user1
        response = TemplateXSDEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_save_xml_content_returns_error(self):
        """test_user_save_xml_content_returns_error

        Returns:

        """
        data = {
            "action": "save",
            "id": "-1",
            "document_id": "-1",
        }
        request = self.factory.post("core_main_app_xsd_text_editor_view", data)
        request.user = self.user1
        response = TemplateXSDEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)


class TestViewBlob(IntegrationBaseTestCase):
    """TestViewBlob"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.user2 = create_mock_user(user_id="2")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlBlobWithMetadataFixture()
        self.fixture.insert_data()

    def test_a_user_can_access_a_blob_if_owner(self):
        """test_a_user_can_access_a_blob_if_owner

        Returns:

        """
        request = self.factory.get("core_main_app_blob_detail")
        request.user = self.user1
        request.GET = {"id": str(self.fixture.blob_1.id)}
        response = ViewBlob.as_view()(request)
        self.assertTrue(
            self.fixture.blob_1.filename in response.content.decode()
        )
        self.assertTrue("Manage Metadata" in response.content.decode())

    def test_a_user_access_a_blob_with_wrong_id_returns_error(self):
        """test_a_user_access_a_blob_with_wrong_id_returns_error

        Returns:

        """
        request = self.factory.get("core_main_app_blob_detail")
        request.user = self.user1
        request.GET = {"id": "1234"}
        response = ViewBlob.as_view()(request)
        self.assertTrue("Error 404" in response.content.decode())

    @patch("core_main_app.components.blob.api.get_by_id")
    def test_a_user_access_a_blob_with_exception_returns_error(
        self, mock_get_by_id
    ):
        """test_a_user_access_a_blob_with_exception_returns_error

        Returns:

        """
        request = self.factory.get("core_main_app_blob_detail")
        request.user = self.user1
        request.GET = {"id": str(self.fixture.blob_1.id)}
        mock_get_by_id.side_effect = Exception()
        response = ViewBlob.as_view()(request)
        self.assertTrue("Error 400" in response.content.decode())

    @patch("core_main_app.access_control.api.check_can_write")
    def test_a_user_can_not_manage_metadata_if_no_write_perm(
        self, mock_check_can_write
    ):
        """test_a_user_can_not_manage_metadata_if_no_write_perm

        Returns:

        """
        request = self.factory.get("core_main_app_blob_detail")
        request.user = self.user2
        mock_check_can_write.side_effect = AccessControlError("Forbidden")
        request.GET = {"id": str(self.fixture.blob_2.id)}
        response = ViewBlob.as_view()(request)
        self.assertTrue("Error" not in response.content.decode())
        self.assertTrue("Manage Metadata" not in response.content.decode())

    def test_an_anonymous_user_can_not_access_a_blob_that_is_not_in_a_workspace(
        self,
    ):
        """test_an_anonymous_user_can_not_access_a_blob_that_is_not_in_a_workspace

        Returns:

        """
        request = self.factory.get("core_main_app_blob_detail")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.blob_1.id)}
        response = ViewBlob.as_view()(request)
        self.assertTrue(
            self.fixture.blob_1.filename not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())

    def test_an_anonymous_user_can_not_access_a_blob_that_is_in_a_private_workspace(
        self,
    ):
        """test_an_anonymous_user_can_not_access_a_blob_that_is_in_a_private_workspace

        Returns:

        """
        request = self.factory.get("core_main_app_blob_detail")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.blob_2.id)}
        response = ViewBlob.as_view()(request)
        self.assertTrue(
            self.fixture.blob_1.filename not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())


class TestManageBlobMetadata(IntegrationBaseTestCase):
    """TestManageBlobMetadata"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.user2 = create_mock_user(user_id="2")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlBlobWithMetadataFixture()
        self.fixture.insert_data()

    def test_a_user_can_access_blob_metadata_if_owner(self):
        """test_a_user_can_access_blob_metadata_if_owner

        Returns:

        """
        request = self.factory.get("core_main_app_blob_metadata")
        request.user = self.user1
        response = ManageBlobMetadata.as_view()(
            request, str(self.fixture.blob_1.id)
        )
        self.assertTrue(
            self.fixture.blob_1.filename in response.content.decode()
        )

    def test_a_user_manage_metadata_with_wrong_id_returns_error(self):
        """test_a_user_manage_metadata_with_wrong_id_returns_error

        Returns:

        """
        request = self.factory.get("core_main_app_blob_metadata")
        request.user = self.user1
        response = ManageBlobMetadata.as_view()(request, "1234")
        self.assertTrue("Error 404" in response.content.decode())

    @patch("core_main_app.components.blob.api.get_by_id")
    def test_a_user_manage_metadata_with_exception_returns_error(
        self, mock_get_by_id
    ):
        """test_a_user_manage_metadata_with_exception_returns_error

        Returns:

        """
        request = self.factory.get("core_main_app_blob_metadata")
        request.user = self.user1
        mock_get_by_id.side_effect = Exception()
        response = ManageBlobMetadata.as_view()(
            request, str(self.fixture.blob_1.id)
        )
        self.assertTrue("Error 400" in response.content.decode())

    @patch("core_main_app.access_control.api.check_can_write")
    def test_a_user_can_not_manage_metadata_if_no_write_perm(
        self, mock_check_can_write
    ):
        """test_a_user_can_not_manage_metadata_if_no_write_perm

        Returns:

        """
        request = self.factory.get("core_main_app_blob_metadata")
        request.user = self.user2
        mock_check_can_write.side_effect = AccessControlError("Forbidden")
        response = ManageBlobMetadata.as_view()(
            request, str(self.fixture.blob_2.id)
        )
        self.assertTrue("Error" not in response.content.decode())

    def test_an_anonymous_user_can_not_access_blob_metadata_if_blob_not_in_a_workspace(
        self,
    ):
        """test_an_anonymous_user_can_not_access_blob_metadata_if_blob_not_in_a_workspace

        Returns:

        """
        request = self.factory.get("core_main_app_blob_metadata")
        request.user = self.anonymous
        response = ManageBlobMetadata.as_view()(
            request, str(self.fixture.blob_1.id)
        )
        self.assertTrue(
            self.fixture.blob_1.filename not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())

    def test_an_anonymous_user_can_not_access_blob_that_is_in_a_private_workspace(
        self,
    ):
        """test_an_anonymous_user_can_not_access_blob_that_is_in_a_private_workspace

        Returns:

        """
        request = self.factory.get("core_main_app_blob_metadata")
        request.user = self.anonymous
        response = ManageBlobMetadata.as_view()(
            request, str(self.fixture.blob_2.id)
        )
        self.assertTrue(
            self.fixture.blob_1.filename not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())


class TestLoadBlobMetadataForm(IntegrationBaseTestCase):
    """TestLoadBlobMetadataForm"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlBlobWithMetadataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_load_blob_metadata_form(self):
        """test_an_anonymous_user_can_not_load_blob_metadata_form

        Returns:

        """
        request = self.factory.get("core_main_blob_metadata_form")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.blob_1)}
        response = LoadBlobMetadataForm.as_view()(request)
        self.assertEqual(response.status_code, 302)

    @patch("core_main_app.components.data.api.get_all_by_user")
    def test_user_can_load_blob_metadata_form(self, mock_get_all_by_user):
        """test_user_can_load_blob_metadata_form

        Returns:

        """
        request = self.factory.get("core_main_blob_metadata_form")
        request.user = self.user1
        request.GET = {"blob_id": str(self.fixture.blob_1.id)}
        mock_get_all_by_user.return_value = []
        response = LoadBlobMetadataForm.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.content.decode())

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @patch("core_main_app.components.data.api.get_all_by_user")
    def test_user_can_load_blob_metadata_form_with_list_of_data(
        self, mock_get_all_by_user, get_all_workspaces_with_read_access_by_user
    ):
        """test_user_can_load_blob_metadata_form_with_list_of_data

        Returns:

        """
        request = self.factory.get("core_main_blob_metadata_form")
        request.user = self.user1
        request.GET = {"blob_id": str(self.fixture.blob_1.id)}
        mock_get_all_by_user.return_value = [self.fixture.data_4]
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        response = LoadBlobMetadataForm.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.content.decode())
        self.assertTrue(self.fixture.data_4.title in response.content.decode())

    @patch("core_main_app.components.blob.api.get_by_id")
    def test_user_can_load_blob_metadata_form_with_model_error(
        self, mock_get_by_id
    ):
        """test_user_can_load_blob_metadata_form_with_model_error

        Returns:

        """
        request = self.factory.get("core_main_blob_metadata_form")
        request.user = self.user1
        request.GET = {"blob_id": str(self.fixture.blob_1.id)}
        mock_get_by_id.side_effect = ModelError("Error")
        response = LoadBlobMetadataForm.as_view()(request)
        self.assertEqual(response.status_code, 400)

    @patch("core_main_app.components.blob.api.get_by_id")
    def test_user_can_load_blob_metadata_form_with_exception(
        self, mock_get_by_id
    ):
        """test_user_can_load_blob_metadata_form_with_exception

        Returns:

        """
        request = self.factory.get("core_main_blob_metadata_form")
        request.user = self.user1
        request.GET = {"blob_id": str(self.fixture.blob_1.id)}
        mock_get_by_id.side_effect = Exception("Error")
        response = LoadBlobMetadataForm.as_view()(request)
        self.assertEqual(response.status_code, 400)


class TestAddMetadataToBlob(IntegrationBaseTestCase):
    """TestAddMetadataToBlob"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlBlobWithMetadataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_add_metadata_to_blob(self):
        """test_an_anonymous_user_can_not_add_metadata_to_blob

        Returns:

        """
        request = self.factory.post("core_main_blob_add_metadata")
        request.user = self.anonymous
        request.POST = {"id": str(self.fixture.blob_1)}
        response = AddMetadataToBlob.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_user_add_metadata_to_blob(self):
        """test_user_add_metadata_to_blob

        Returns:

        """
        request = self.factory.post("core_main_blob_metadata_form")
        request.user = self.user1
        request.POST = QueryDict("").copy()
        request.POST.update({"blob_id": str(self.fixture.blob_1.id)})
        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)
        middleware = MessageMiddleware(mock_get_response)
        middleware.process_request(request)
        request.session.save()
        response = AddMetadataToBlob.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_add_metadata_to_blob_with_list_of_ids(self):
        """test_user_add_metadata_to_blob

        Returns:

        """
        request = self.factory.post("core_main_blob_metadata_form")
        request.user = self.user1
        request.POST = QueryDict("").copy()
        request.POST.update({"blob_id": str(self.fixture.blob_1.id)})
        request.POST.update({"metadata_id[]": str(self.fixture.data_4.id)})
        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)
        middleware = MessageMiddleware(mock_get_response)
        middleware.process_request(request)
        request.session.save()
        response = AddMetadataToBlob.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch("core_main_app.components.blob.api.get_by_id")
    def test_user_can_not_add_metadata_to_blob_with_model_error(
        self, mock_get_by_id
    ):
        """test_user_can_not_add_metadata_to_blob_with_model_error

        Returns:

        """
        request = self.factory.post("core_main_blob_add_metadata")
        request.user = self.user1
        request.POST = QueryDict("").copy()
        request.POST.update({"blob_id": str(self.fixture.blob_1.id)})
        mock_get_by_id.side_effect = ModelError("Error")
        response = AddMetadataToBlob.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Blob not found.")

    @patch("core_main_app.components.blob.api.get_by_id")
    def test_user_can_not_add_metadata_to_blob_with_acl_error(
        self, mock_get_by_id
    ):
        """test_user_can_not_add_metadata_to_blob_with_model_error

        Returns:

        """
        request = self.factory.post("core_main_blob_add_metadata")
        request.user = self.user1
        request.POST = QueryDict("").copy()
        request.POST.update({"blob_id": str(self.fixture.blob_1.id)})
        mock_get_by_id.side_effect = AccessControlError("Error")
        response = AddMetadataToBlob.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Permission denied.")

    @patch("core_main_app.components.blob.api.get_by_id")
    def test_user_can_not_add_metadata_to_blob_with_model_exception(
        self, mock_get_by_id
    ):
        """test_user_can_not_add_metadata_to_blob_with_model_exception

        Returns:

        """
        request = self.factory.post("core_main_blob_add_metadata")
        request.user = self.user1
        request.POST = QueryDict("").copy()
        request.POST.update({"blob_id": str(self.fixture.blob_1.id)})
        mock_get_by_id.side_effect = Exception("Error")
        response = AddMetadataToBlob.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"An unexpected error occurred.")


class TestRemoveMetadataFromBlob(IntegrationBaseTestCase):
    """TestRemoveMetadataFromBlob"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlBlobWithMetadataFixture()
        self.fixture.insert_data()

    def test_an_anonymous_user_can_not_remove_metadata_from_blob(self):
        """test_an_anonymous_user_can_not_remove_metadata_from_blob

        Returns:

        """
        request = self.factory.post("core_main_blob_remove_metadata")
        request.user = self.anonymous
        request.POST = {"id": str(self.fixture.blob_1)}
        response = RemoveMetadataFromBlob.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_user_remove_metadata_from_blob(self):
        """test_user_remove_metadata_from_blob

        Returns:

        """
        request = self.factory.post("core_main_blob_remove_metadata")
        request.user = self.user1
        request.POST = QueryDict("").copy()
        request.POST.update({"blob_id": str(self.fixture.blob_1.id)})
        request.POST.update({"metadata_id": str(self.fixture.data_1.id)})
        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)
        middleware = MessageMiddleware(mock_get_response)
        middleware.process_request(request)
        request.session.save()
        response = RemoveMetadataFromBlob.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch("core_main_app.components.blob.api.get_by_id")
    def test_user_can_not_remove_metadata_to_blob_with_model_error(
        self, mock_get_by_id
    ):
        """test_user_can_not_remove_metadata_to_blob_with_model_error

        Returns:

        """
        request = self.factory.post("core_main_blob_remove_metadata")
        request.user = self.user1
        request.POST = QueryDict("").copy()
        request.POST.update({"blob_id": str(self.fixture.blob_1.id)})
        mock_get_by_id.side_effect = ModelError("Error")
        response = RemoveMetadataFromBlob.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Blob not found.")

    @patch("core_main_app.components.blob.api.get_by_id")
    def test_user_can_not_remove_metadata_to_blob_with_acl_error(
        self, mock_get_by_id
    ):
        """test_user_can_not_remove_metadata_to_blob_with_acl_error

        Returns:

        """
        request = self.factory.post("core_main_blob_remove_metadata")
        request.user = self.user1
        request.POST = QueryDict("").copy()
        request.POST.update({"blob_id": str(self.fixture.blob_1.id)})
        mock_get_by_id.side_effect = AccessControlError("Error")
        response = RemoveMetadataFromBlob.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Permission denied.")

    @patch("core_main_app.components.blob.api.get_by_id")
    def test_user_can_not_remove_metadata_to_blob_with_model_exception(
        self, mock_get_by_id
    ):
        """test_user_can_not_remove_metadata_to_blob_with_model_exception

        Returns:

        """
        request = self.factory.post("core_main_blob_remove_metadata")
        request.user = self.user1
        request.POST = QueryDict("").copy()
        request.POST.update({"blob_id": str(self.fixture.blob_1.id)})
        mock_get_by_id.side_effect = Exception("Error")
        response = RemoveMetadataFromBlob.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"An unexpected error occurred.")


class TestUploadFile(IntegrationBaseTestCase):
    """TestUploadFile"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = AccessControlBlobWithMetadataFixture()
        self.fixture.insert_data()
        self.file = SimpleUploadedFile(name="test.txt", content=b"test")

    def test_an_anonymous_user_can_not_upload_file(self):
        """test_an_anonymous_user_can_not_upload_file

        Returns:

        """
        request = self.factory.post("core_main_upload_file")
        request.user = self.anonymous
        request.FILES["file"] = self.file
        response = UploadFile.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_user_can_upload_file(self):
        """test_user_can_upload_file

        Returns:

        """
        request = self.factory.post("core_main_upload_file")
        request.user = self.user1
        request.FILES["file"] = self.file
        mock_get_response = MagicMock()
        # Add middlewares
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)
        middleware = MessageMiddleware(mock_get_response)
        middleware.process_request(request)
        response = UploadFile.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch("core_main_app.components.blob.api.insert")
    def test_user_can_not_upload_file_with_error(self, mock_insert):
        """test_user_can_not_upload_file_with_error

        Returns:

        """
        request = self.factory.post("core_main_upload_file")
        request.user = self.user1
        request.FILES["file"] = self.file
        mock_insert.side_effect = Exception()
        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)
        middleware = MessageMiddleware(mock_get_response)
        middleware.process_request(request)
        response = UploadFile.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_can_not_upload_file_with_invalid_form(self):
        """test_user_can_not_upload_file_with_invalid_form

        Returns:

        """
        request = self.factory.post("core_main_upload_file")
        request.user = self.user1
        request.FILES["file"] = 123
        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)
        middleware = MessageMiddleware(mock_get_response)
        middleware.process_request(request)
        response = UploadFile.as_view()(request)
        self.assertEqual(response.status_code, 400)


class TestDataJSONEditorView(IntegrationBaseTestCase):
    """Test Post Data JSON Editor View"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.user2 = create_mock_user(user_id="2")
        self.anonymous = AnonymousUser()
        self.fixture = JSONDataFixtures()
        self.fixture.insert_data()

    def test_prepare_context_returns_context(self):
        """test_prepare_context_returns_context

        Returns:

        """
        request = self.factory.get("core_main_app_json_text_editor_view")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.data_1.id)}
        data_editor = DataJSONEditor()
        data_editor.request = request
        context = data_editor._prepare_context(self.fixture.data_1)
        self.assertEqual(context["page_title"], "JSON Text Editor")
        self.assertEqual(context["name"], self.fixture.data_1.title)
        self.assertEqual(context["type"], "JSON")
        self.assertEqual(context["document_id"], self.fixture.data_1.id)
        self.assertEqual(context["document_name"], "Data")
        self.assertEqual(
            context["template_id"], self.fixture.data_1.template.id
        )

    def test_user_can_not_access_to_data_without_id(self):
        """test_user_can_not_access_to_data_without_id

        Returns:

        """
        request = self.factory.get("core_main_app_json_text_editor_view")
        request.user = self.user1
        response = DataJSONEditor.as_view()(request)
        self.assertTrue("Error 400" in response.content.decode())

    def test_anonymous_user_can_not_access_to_data(self):
        """test_anonymous_user_can_not_access_to_data

        Returns:

        """
        request = self.factory.get("core_main_app_json_text_editor_view")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.data_1.id)}
        response = DataJSONEditor.as_view()(request)
        self.assertTrue(
            self.fixture.data_1.title not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())

    def test_user_can_not_access_to_data_if_not_found(self):
        """test_user_can_not_access_a_data_if_not_found

        Returns:

        """
        request = self.factory.get("core_main_app_json_text_editor_view")
        request.GET = {"id": "-1"}
        request.user = self.user1
        response = DataJSONEditor.as_view()(request)
        self.assertTrue("Error 404" in response.content.decode())

    def test_user_can_access_to_data_if_owner(self):
        """test_user_can_access_a_data_if_owner

        Returns:

        """
        request = self.factory.get("core_main_app_json_text_editor_view")
        request.GET = {"id": str(self.fixture.data_1.id)}
        request.user = self.user1
        response = DataJSONEditor.as_view()(
            request,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_format_json_content(self):
        """test_user_can_format_xml_content

        Returns:

        """
        data = {
            "content": "{}",
            "action": "format",
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )

        request.user = self.user1
        response = DataJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_validate_json_content(self):
        """test_user_can_validate_json_content

        Returns:

        """
        data = {
            "content": "{}",
            "action": "validate",
            "template_id": str(self.fixture.data_1.template.id),
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )

        request.user = self.user1
        response = DataJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_validate_bad_json_content_returns_error(self):
        """test_user_validate_bad_json_content_returns_error

        Returns:

        """
        data = {
            "content": "<bad></format>",
            "action": "validate",
            "template_id": str(self.fixture.data_1.template.id),
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user1

        response = DataJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_validate_empty_content_returns_error(self):
        """test_user_validate_empty_content_returns_error

        Returns:

        """
        data = {
            "content": "",
            "action": "validate",
            "template_id": str(self.fixture.data_1.template.id),
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )

        request.user = self.user1
        response = DataJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_validate_json_content_returns_error(self):
        """test_user_validate_json_content_returns_error

        Returns:

        """
        data = {
            "content": "{}",
            "action": "validate",
            "template_id": "",
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user1
        response = DataJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_can_save_json_content(self):
        """test_user_can_save_json_content

        Returns:

        """
        data = {
            "content": '{"test":"1"}',
            "action": "save",
            "document_id": str(self.fixture.data_1.id),
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user1
        response = DataJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_save_json_content_returns_acl_error(self):
        """test_user_save_json_content_returns_acl_error

        Returns:

        """
        data = {
            "content": "{}",
            "action": "save",
            "document_id": str(self.fixture.data_1.id),
            "id": str(self.fixture.data_1.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user2
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        response = DataJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_user_save_json_content_returns_dne_error(self):
        """test_user_save_json_content_returns_dne_error

        Returns:

        """
        data = {
            "content": "{}",
            "action": "save",
            "document_id": "-1",
            "id": "-1",
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user1
        response = DataJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_save_json_content_returns_error(self):
        """test_user_save_json_content_returns_error

        Returns:

        """
        data = {
            "action": "save",
            "document_id": "-1",
            "id": "-1",
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user1
        response = DataJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    @patch("core_main_app.utils.file.get_byte_size_from_string")
    def test_json_content_too_big_returns_error(self, mock_get_byte_size):
        """test_json_content_too_big_returns_error

        Returns:

        """
        mock_get_byte_size.return_value = MAX_DOCUMENT_EDITING_SIZE + 1
        request = self.factory.get("core_main_app_json_text_editor_view")
        request.GET = {"id": str(self.fixture.data_1.id)}
        request.user = self.user1
        response = DataJSONEditor.as_view()(request)
        self.assertTrue(
            "MAX_DOCUMENT_EDITING_SIZE" in response.content.decode()
        )

    def test_generate_raises_not_implemented_error(self):
        """test_generate_raises_not_implemented_error

        Returns:

        """
        # Assert
        with self.assertRaises(NotImplementedError):
            DataJSONEditor.generate(self)


class TestTemplateJSONEditorView(IntegrationBaseTestCase):
    """Test JSON Text Editor View"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.user2 = create_mock_user(user_id="2")
        self.anonymous = AnonymousUser()
        self.fixture = JSONDataFixtures()
        self.fixture.insert_data()

    def test_anonymous_user_can_not_access_template_content(self):
        """test_anonymous_user_can_not_access_template_content

        Returns:

        """
        request = self.factory.get("core_main_app_json_text_editor_view")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.template.id)}
        response = TemplateJSONEditor.as_view()(request)

        self.assertTrue("Error 403" in response.content.decode())

    def test_user_can_not_access_template_if_not_found(self):
        """test_user_can_not_access_template_if_not_found

        Returns:

        """
        request = self.factory.get("core_main_app_json_text_editor_view")
        request.user = self.user1
        request.GET = {"id": "-1"}
        response = TemplateJSONEditor.as_view()(request)
        self.assertTrue("Error 404" in response.content.decode())

    def test_user_can_access_template(self):
        """test_user_can_access_template

        Returns:

        """
        request = self.factory.get("core_main_app_json_text_editor_view")
        request.user = self.user1
        request.GET = {"id": str(self.fixture.template.id)}
        response = TemplateJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_format_json_content(self):
        """test_user_can_format_json_content

        Returns:

        """
        data = {
            "content": self.fixture.template.content,
            "action": "format",
            "id": str(self.fixture.template.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )

        request.user = self.user1
        response = TemplateJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_validate_json_content(self):
        """test_user_can_validate_json_content

        Returns:

        """
        data = {
            "content": self.fixture.template.content,
            "action": "validate",
            "template_id": str(self.fixture.template.id),
            "id": str(self.fixture.template.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user1
        response = TemplateJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_validate_empty_json_content_returns_error(self):
        """test_user_validate_empty_json_content_returns_error

        Returns:

        """
        data = {
            "content": "",
            "action": "validate",
            "template_id": str(self.fixture.template.id),
            "id": str(self.fixture.template.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user1
        response = TemplateJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_validate_bad_json_content_returns_error(self):
        """test_user_validate_bad_json_content_returns_error

        Returns:

        """
        content = (
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            '<xs:element nam="root"></xs:element></xs:schema>'
        )
        data = {
            "content": content,
            "action": "validate",
            "template_id": str(self.fixture.template.id),
            "id": str(self.fixture.template.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user1
        response = TemplateJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_can_save_json_content(self):
        """test_user_can_save_json_content

        Returns:

        """

        data = {
            "content": "{}",
            "action": "save",
            "id": str(self.fixture.template.id),
            "document_id": str(self.fixture.template.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user1
        response = TemplateJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_save_json_content_returns_acl_error(self):
        """test_user_save_json_content_returns_acl_error

        Returns:

        """
        data = {
            "content": "{}",
            "action": "save",
            "id": str(self.fixture.template.id),
            "document_id": str(self.fixture.template.id),
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user2
        response = TemplateJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_user_save_json_content_returns_dne_error(self):
        """test_user_save_json_content_returns_dne_error

        Returns:

        """
        data = {
            "content": "{}",
            "action": "save",
            "id": "-1",
            "document_id": "-1",
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user1
        response = TemplateJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_save_json_content_returns_error(self):
        """test_user_save_json_content_returns_error

        Returns:

        """
        data = {
            "action": "save",
            "id": "-1",
            "document_id": "-1",
        }
        request = self.factory.post(
            "core_main_app_json_text_editor_view", data
        )
        request.user = self.user1
        response = TemplateJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    @patch("core_main_app.utils.file.get_byte_size_from_string")
    def test_json_content_too_big_returns_error(self, mock_get_byte_size):
        """test_json_content_too_big_returns_error

        Returns:

        """
        mock_get_byte_size.return_value = MAX_DOCUMENT_EDITING_SIZE + 1
        request = self.factory.get("core_main_app_json_text_editor_view")
        request.GET = {"id": str(self.fixture.template.id)}
        request.user = self.user1
        response = TemplateJSONEditor.as_view()(request)
        self.assertTrue(
            "MAX_DOCUMENT_EDITING_SIZE" in response.content.decode()
        )
