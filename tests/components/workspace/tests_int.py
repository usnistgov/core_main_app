""" Integration Test for Workspace API
"""
from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    MongoIntegrationTransactionTestCase,
)
from tests.components.user.fixtures.fixtures import UserFixtures
from tests.components.workspace.fixtures.fixtures import WorkspaceFixtures

TITLE_1 = "title 1"


class TestCreateWorkspace(MongoIntegrationTransactionTestCase):
    def test_create_one_workspace(self):
        # Context
        user1 = UserFixtures().create_user()
        # Act
        workspace = workspace_api.create_and_save(TITLE_1, user1.id)
        # Assert
        self.assertEqual(workspace.title, TITLE_1)
        self.assertEqual(workspace.owner, str(user1.id))

    def test_create_two_workspaces_same_name_same_user(self):
        # Context
        user1 = UserFixtures().create_user()
        # Act
        workspace_api.create_and_save(TITLE_1, user1.id)
        with self.assertRaises(exceptions.NotUniqueError):
            workspace_api.create_and_save(TITLE_1, user1.id)

    def test_create_two_workspaces_same_name_different_case_same_user(self):
        # Context
        user1 = UserFixtures().create_user()
        # Act
        workspace_api.create_and_save(TITLE_1, user1.id)
        with self.assertRaises(exceptions.NotUniqueError):
            workspace_api.create_and_save(TITLE_1.upper(), user1.id)

    def test_create_two_workspaces_same_name_different_user(self):
        # Context
        number_workspace = len(workspace_api.get_all())
        user1 = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        # Act
        workspace_api.create_and_save(TITLE_1, user1.id)
        workspace_api.create_and_save(TITLE_1, user2.id)
        # Assert
        self.assertEqual(number_workspace + 2, len(workspace_api.get_all()))

    def test_create_workspace_without_owner(self):
        # Act
        workspace = workspace_api.create_and_save(TITLE_1)
        # Assert
        self.assertEqual(workspace.title, TITLE_1)
        self.assertIsNone(workspace.owner)


class TestIsWorkspaceGlobal(MongoIntegrationTransactionTestCase):
    """Test Is Workspace Global"""

    def test_is_workspace_global_true(self):
        # Context
        workspace = WorkspaceFixtures.create_global_workspace(TITLE_1)
        # Act
        result = workspace_api.is_workspace_global(workspace)
        # Assert
        self.assertTrue(result)

    def test_is_workspace_global_false(self):
        # Context
        workspace = WorkspaceFixtures.create_workspace("1", TITLE_1)
        # Act
        result = workspace_api.is_workspace_global(workspace)
        # Assert
        self.assertFalse(result)


class TestGetGlobalWorkspace(MongoIntegrationTransactionTestCase):
    """Test Get Global Workspace"""

    def test_get_global_workspace(self):
        # Context
        workspace = WorkspaceFixtures.create_global_workspace(TITLE_1)
        # Act
        result = workspace_api.get_global_workspace()
        # Assert
        self.assertEquals(workspace, result)

    def test_get_global_workspace_multiple_workspace(self):
        # Context
        global_workspace = WorkspaceFixtures.create_global_workspace(TITLE_1)
        workspace = WorkspaceFixtures.create_workspace("1", TITLE_1)
        # Act
        result = workspace_api.get_global_workspace()
        # Assert
        self.assertEquals(global_workspace, result)

    def test_get_global_workspace_not_global(self):
        # Context
        WorkspaceFixtures.create_workspace("1", TITLE_1)
        # Act
        with self.assertRaises(exceptions.DoesNotExist):
            workspace_api.get_global_workspace()


class TestCheckIfWorkspaceCanBeChanged(MongoIntegrationTransactionTestCase):
    """Test Check If Workspace Can Be Changed"""

    def test_check_if_workspace_can_be_changed_return_true_if_workspace_is_none_and_allow_public_is_false(
        self,
    ):
        # A global workspace is public
        data = Data(
            template=Template(),
            user_id="1",
            dict_content=None,
            title="title",
            workspace=None,
        )

        # Act
        result = workspace_api.check_if_workspace_can_be_changed(data, False)
        # Assert
        self.assertEquals(result, True)

    def test_check_if_workspace_can_be_changed_return_true_if_workspace_is_none_and_allow_public_is_true(
        self,
    ):
        # A global workspace is public
        data = Data(
            template=Template(),
            user_id="1",
            dict_content=None,
            title="title",
            workspace=None,
        )

        # Act
        result = workspace_api.check_if_workspace_can_be_changed(data, True)
        # Assert
        self.assertEquals(result, True)

    def test_check_if_workspace_can_be_changed_return_false_if_workspace_is_public_and_allow_public_is_false(
        self,
    ):
        # A global workspace is public
        workspace = WorkspaceFixtures.create_global_workspace(TITLE_1)
        data = Data(
            template=Template(),
            user_id="1",
            dict_content=None,
            title="title",
            workspace=workspace,
        )

        # Act
        result = workspace_api.check_if_workspace_can_be_changed(data, False)
        # Assert
        self.assertEquals(result, False)

    def test_check_if_workspace_can_be_changed_return_true_if_workspace_is_public_and_allow_public_is_true(
        self,
    ):
        # A global workspace is public
        workspace = WorkspaceFixtures.create_global_workspace(TITLE_1)
        data = Data(
            template=Template(),
            user_id="1",
            dict_content=None,
            title="title",
            workspace=workspace,
        )
        # Act
        result = workspace_api.check_if_workspace_can_be_changed(data, True)
        # Assert
        self.assertEquals(result, True)
