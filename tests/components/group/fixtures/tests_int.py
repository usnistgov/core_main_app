""" Integration Test for Group Fixtures
"""

from tests.components.group.fixtures.fixtures import GroupFixtures

from core_main_app.components.group import api as group_api
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    MongoIntegrationTransactionTestCase,
)


class TestGroupFixtures(MongoIntegrationTransactionTestCase):
    """Test Group fixtures"""

    def test_create_group(self):
        """test create group

        Returns:

        """
        # Context
        group_count = len(group_api.get_all_groups())
        self.assertEqual(
            group_count, 2
        )  # default and anonymous are created when launching the tests

        # Act
        GroupFixtures().create_group(name="test name")

        # Assert
        list_groups = group_api.get_all_groups()
        self.assertEqual(len(list_groups), group_count + 1)
