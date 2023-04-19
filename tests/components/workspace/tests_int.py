""" Integration Test for Workspace API
"""
from tests.components.user.fixtures.fixtures import UserFixtures
from tests.components.workspace.fixtures.fixtures import WorkspaceFixtures

from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)

TITLE_1 = "title 1"


class TestCreateWorkspace(IntegrationTransactionTestCase):
    """TestCreateWorkspace"""

    def test_create_one_workspace(self):
        """test create one workspace

        Returns:

        """
        # Context
        user1 = UserFixtures().create_user()
        # Act
        workspace = workspace_api.create_and_save(TITLE_1, user1.id)
        # Assert
        self.assertEqual(workspace.title, TITLE_1)
        self.assertEqual(workspace.owner, str(user1.id))

    def test_create_two_workspaces_same_name_same_user(self):
        """test create two workspaces same name same user

        Returns:

        """
        # Context
        user1 = UserFixtures().create_user()
        # Act
        workspace_api.create_and_save(TITLE_1, user1.id)
        with self.assertRaises(exceptions.NotUniqueError):
            workspace_api.create_and_save(TITLE_1, user1.id)

    def test_create_two_workspaces_same_name_different_case_same_user(self):
        """test create two workspaces same name different case same user

        Returns:

        """
        # Context
        user1 = UserFixtures().create_user()
        # Act
        workspace_api.create_and_save(TITLE_1, user1.id)
        with self.assertRaises(exceptions.NotUniqueError):
            workspace_api.create_and_save(TITLE_1.upper(), user1.id)

    def test_create_two_workspaces_same_name_different_user(self):
        """test create two workspaces same name different user

        Returns:

        """
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
        """test create workspace without owner

        Returns:

        """
        # Act
        workspace = workspace_api.create_and_save(TITLE_1)
        # Assert
        self.assertEqual(workspace.title, TITLE_1)
        self.assertIsNone(workspace.owner)


class TestIsWorkspaceGlobal(IntegrationTransactionTestCase):
    """Test Is Workspace Global"""

    def test_is_workspace_global_true(self):
        """test is workspace global true

        Returns:

        """
        # Context
        workspace = WorkspaceFixtures.create_global_workspace(TITLE_1)
        # Act
        result = workspace_api.is_workspace_global(workspace)
        # Assert
        self.assertTrue(result)

    def test_is_workspace_global_false(self):
        """test is workspace global false

        Returns:

        """
        # Context
        workspace = WorkspaceFixtures.create_workspace("1", TITLE_1)
        # Act
        result = workspace_api.is_workspace_global(workspace)
        # Assert
        self.assertFalse(result)


class TestGetGlobalWorkspace(IntegrationTransactionTestCase):
    """Test Get Global Workspace"""

    def test_get_global_workspace(self):
        """test get global workspace

        Returns:

        """
        # Context
        workspace = WorkspaceFixtures.create_global_workspace(TITLE_1)
        # Act
        result = workspace_api.get_global_workspace()
        # Assert
        self.assertEqual(workspace, result)

    def test_get_global_workspace_multiple_workspace(self):
        """test get global workspace multiple workspace

        Returns:

        """
        # Context
        global_workspace = WorkspaceFixtures.create_global_workspace(TITLE_1)
        WorkspaceFixtures.create_workspace("1", TITLE_1)
        # Act
        result = workspace_api.get_global_workspace()
        # Assert
        self.assertEqual(global_workspace, result)

    def test_get_global_workspace_not_global(self):
        """test get global workspace not global

        Returns:

        """
        # Context
        WorkspaceFixtures.create_workspace("1", TITLE_1)
        # Act
        with self.assertRaises(exceptions.DoesNotExist):
            workspace_api.get_global_workspace()


class TestCheckIfWorkspaceCanBeChanged(IntegrationTransactionTestCase):
    """Test Check If Workspace Can Be Changed"""

    def test_workspace_can_be_changed_return_true_if_workspace_is_none_and_allow_public_is_false(
        self,
    ):
        """test workspace can be changed return true if workspace is none and allow public is false

        Returns:

        """
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
        self.assertEqual(result, True)

    def test_workspace_can_be_changed_return_true_if_workspace_is_none_and_allow_public_is_true(
        self,
    ):
        """test workspace can be changed return true if workspace is none and allow public is false

        Returns:

        """
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
        self.assertEqual(result, True)

    def test_workspace_can_be_changed_return_false_if_workspace_is_public_and_allow_public_is_false(
        self,
    ):
        """test workspace can be changed return false if workspace is public
        and allow public is false

        Returns:

        """
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
        self.assertEqual(result, False)

    def test_workspace_can_be_changed_return_true_if_workspace_is_public_and_allow_public_is_true(
        self,
    ):
        """test workspace can be changed return true if workspace is public and allow public is true

        Returns:

        """
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
        self.assertEqual(result, True)
