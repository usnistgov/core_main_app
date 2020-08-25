""" Fixtures files for Group
"""
from core_main_app.components.group import api as group_api
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface


class GroupFixtures(FixtureInterface):
    """Group Fixture"""

    def insert_data(self):
        pass

    @staticmethod
    def create_group(name="name"):
        group, created = group_api.get_or_create(name=name)
        return group
