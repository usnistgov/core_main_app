""" Fixtures files for Workspace
"""

from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_main_app.components.workspace import api as workspace_api


class WorkspaceFixtures(FixtureInterface):
    """ Workspace Fixture
    """
    def insert_data(self):
        pass

    @staticmethod
    def create_workspace(owner_id, title):
        return workspace_api.create_and_save(owner_id, title)
