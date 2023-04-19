""" Integration Test for Workspace Fixtures
"""

from tests.components.workspace.fixtures.fixtures import WorkspaceFixtures

from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)

TITLE = "title"


class TestWorkspaceFixtures(IntegrationTransactionTestCase):
    """Test Workspace fixtures"""

    def test_create_workspace(self):
        """test create workspace

        Returns:

        """
        # Context
        workspace_count = len(workspace_api.get_all())
        self.assertEqual(workspace_count, 0)

        # Act
        WorkspaceFixtures().create_workspace("1", TITLE)

        # Assert
        list_workspace = workspace_api.get_all()
        self.assertEqual(list_workspace[0].title, TITLE)
        self.assertEqual(len(list_workspace), workspace_count + 1)
