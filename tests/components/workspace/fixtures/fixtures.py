""" Fixtures files for Workspace
"""

from core_main_app.components.group import api as group_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.permissions import api as permission_api
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class WorkspaceFixtures(FixtureInterface):
    """Workspace Fixture"""

    def insert_data(self):
        """insert data

        Returns:

        """

        pass

    @staticmethod
    def create_workspace(owner_id, title):
        """create workspace

        Args:
            owner_id:
            title:

        Returns:

        """
        return workspace_api.create_and_save(title, owner_id)

    @staticmethod
    def create_global_workspace(title):
        """create global workspace

        Args:
            title:

        Returns:

        """
        workspace = workspace_api.create_and_save(title, is_public=True)
        permission_api.add_permission_to_group(
            group_api.get_anonymous_group(), workspace.read_perm_id
        )
        permission_api.add_permission_to_group(
            group_api.get_default_group(), workspace.read_perm_id
        )
        return workspace
