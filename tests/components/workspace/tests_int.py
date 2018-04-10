""" Integration Test for Workspace API
"""
from core_main_app.commons import exceptions
from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import \
    MongoIntegrationTransactionTestCase
from tests.components.user.fixtures.fixtures import UserFixtures

TITLE_1 = 'title 1'


class TestCreateWorkspace(MongoIntegrationTransactionTestCase):

    def test_create_one_workspace(self):
        # Context
        user1 = UserFixtures().create_user()
        # Act
        workspace = workspace_api.create_and_save(user1.id, TITLE_1)
        # Assert
        self.assertEqual(workspace.title, TITLE_1)
        self.assertEqual(workspace.owner, str(user1.id))

    def test_create_two_workspaces_same_name_same_user(self):
        # Context
        user1 = UserFixtures().create_user()
        # Act
        workspace_api.create_and_save(user1.id, TITLE_1)
        with self.assertRaises(exceptions.NotUniqueError):
            workspace_api.create_and_save(user1.id, TITLE_1)

    def test_create_two_workspaces_same_name_different_case_same_user(self):
        # Context
        user1 = UserFixtures().create_user()
        # Act
        workspace_api.create_and_save(user1.id, TITLE_1)
        with self.assertRaises(exceptions.NotUniqueError):
            workspace_api.create_and_save(user1.id, TITLE_1.upper())

    def test_create_two_workspaces_same_name_different_user(self):
        # Context
        number_workspace = len(workspace_api.get_all())
        user1 = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        # Act
        workspace_api.create_and_save(user1.id, TITLE_1)
        workspace_api.create_and_save(user2.id, TITLE_1)
        # Assert
        self.assertEqual(number_workspace + 2, len(workspace_api.get_all()))
