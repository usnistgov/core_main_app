""" Test access to views
"""
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from core_main_app.components.blob import api as blob_api
from core_main_app.components.data import api as data_api
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.views.common.views import (
    ViewData,
    EditWorkspaceRights,
    TemplateXSLRenderingView,
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
)
from core_main_app.views.user.views import manage_template_versions
from tests.views.fixtures import AccessControlDataFixture
from tests.test_settings import LOGIN_URL


class TestViewData(MongoIntegrationBaseTestCase):
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

    def test_an_anonymous_user_can_not_access_a_data_that_is_not_in_a_workspace(self):
        """test_an_anonymous_user_can_not_access_a_data_that_is_not_in_a_workspace

        Returns:

        """
        request = self.factory.get("core_main_app_data_detail")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.data_1.id)}
        response = ViewData.as_view()(request)
        self.assertTrue(self.fixture.data_1.title not in response.content.decode())
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
        self.assertTrue(self.fixture.data_1.title not in response.content.decode())
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
            self.fixture.data_public_workspace.title not in response.content.decode()
        )
        self.assertTrue("Error" in response.content.decode())


class TestManageTemplateVersions(MongoIntegrationBaseTestCase):
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


class TestTemplateXSLRenderingView(MongoIntegrationBaseTestCase):
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


class TestAssignDataView(MongoIntegrationBaseTestCase):
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


class TestAssignBlobView(MongoIntegrationBaseTestCase):
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


class TestChangeDataDisplayView(MongoIntegrationBaseTestCase):
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
        data = {"xslt_id": "id", "data_id": str(self.fixture.data_workspace_1.id)}
        request = self.factory.post("core_main_add_change_data_display", data)
        request.user = self.anonymous
        response = change_data_display(request)
        self.assertEqual(response.status_code, 403)

    def test_an_anonymous_user_can_not_assign_a_public_workspace_data(self):
        """test_an_anonymous_user_can_not_assign_a_public_workspace_data

        Returns:

        """
        data = {"xslt_id": "id", "data_id": str(self.fixture.data_public_workspace.id)}
        request = self.factory.post("core_main_add_change_data_display", data)
        request.user = self.anonymous
        response = change_data_display(request)
        self.assertEqual(response.status_code, 403)


class TestEditRights(MongoIntegrationBaseTestCase):
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


class TestLoadFormChangeWorkspace(MongoIntegrationBaseTestCase):
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


class TestLoadAddUserForm(MongoIntegrationBaseTestCase):
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


class TestAddUserToWorkspace(MongoIntegrationBaseTestCase):
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


class TestSwitchRight(MongoIntegrationBaseTestCase):
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


class TestRemoveRights(MongoIntegrationBaseTestCase):
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


class TestAddGroupForm(MongoIntegrationBaseTestCase):
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


class TestAddGroupRightToWorkspace(MongoIntegrationBaseTestCase):
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
