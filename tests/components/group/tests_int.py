""" Integration Test for Group
"""

from tests.components.group.fixtures.fixtures import GroupFixtures
from django.contrib.auth.models import Group
from core_main_app.components.group import api as group_api
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)


class TestGetAllGroups(IntegrationTransactionTestCase):
    """Test Get All Groups"""

    def test_get_all_groups_returns_default_groups(self):
        """test_get_all_groups_returns_default_groups

        Returns:

        """
        # Act
        result = group_api.get_all_groups()

        # Assert
        self.assertEqual(len(result), 2)

    def test_get_all_groups_returns_group_list(self):
        """test_get_all_groups_returns_group_list

        Returns:

        """
        # Arrange
        GroupFixtures().create_group(name="test name")

        # Act
        list_groups = group_api.get_all_groups()

        # Assert
        self.assertEqual(len(list_groups), 3)
        self.assertTrue(all(isinstance(group, Group) for group in list_groups))


class TestGetGroupByNameAndPermission(IntegrationTransactionTestCase):
    """Test Get Group By Name And Permission"""

    def test_get_group_by_name_and_permission_returns_group_list(self):
        """test get group by name and permission returns group list

        Returns:

        """
        # Arrange
        group = GroupFixtures().create_group(name="test name")

        # Act
        result = group_api.get_by_name_and_permission(group.name, None)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertTrue(group in result)

    def test_get_group_by_name_and_permission_returns_empty_list_if_group_does_not_exist(
        self,
    ):
        """test get group by name and permission returns empty list if group does not exist

        Returns:

        """

        # Act
        result = group_api.get_by_name_and_permission("", None)

        # Assert
        self.assertEqual(len(result), 0)

    def test_get_group_by_name_and_wrong_permission_returns_empty_list(self):
        """test get group by name and wrong permission returns empty list

        Returns:

        """

        # Arrange
        group = GroupFixtures().create_group(name="test name")

        # Act
        result = group_api.get_by_name_and_permission(group.name, "Wrong")

        # Assert
        self.assertEqual(len(result), 0)


class TestGetAllGroupByListId(IntegrationTransactionTestCase):
    """Test Get All Group By List Id"""

    def test_get_all_groups_by_list_id_returns_list(self):
        """test get all groups by list id returns list

        Returns:

        """
        # Act
        result = group_api.get_all_groups_by_list_id([1, 2])

        # Assert
        self.assertEqual(len(result), 2)

    def test_get_all_groups_by_invalid_list_id_returns_empty_list(self):
        """test get all groups by invalid list id returns empty list

        Returns:

        """
        # Act
        result = group_api.get_all_groups_by_list_id([0, -1])

        # Assert
        self.assertEqual(len(result), 0)

    def test_get_all_groups_by_list_id_returns_valid_id_group_list(self):
        """test get all groups by invalid list id returns empty list

        Returns:

        """
        # Act
        result = group_api.get_all_groups_by_list_id([1, -1])

        # Assert
        self.assertEqual(len(result), 1)


class TestGetAllGroupExceptListId(IntegrationTransactionTestCase):
    """Test Get All Group Except List Id"""

    def test_get_all_groups_except_list_id_returns_list(self):
        """test get all groups except list id returns list

        Returns:

        """
        # Arrange
        GroupFixtures().create_group(name="test name")

        # Act
        result = group_api.get_all_groups_except_list_id([1, 2])

        # Assert
        self.assertEqual(len(result), 1)

    def test_get_all_groups_except_all_available_group_ids_returns_empty_list(
        self,
    ):
        """test get all groups except all available group ids returns empty list

        Returns:

        """
        # Act
        result = group_api.get_all_groups_except_list_id([1, 2])

        # Assert
        self.assertEqual(len(result), 0)


class TestGetAllGroupExceptList(IntegrationTransactionTestCase):
    """Test Get All Group Except List"""

    def test_get_all_groups_except_list_returns_list(self):
        """test get all groups except list returns list

        Returns:

        """
        # Arrange
        group = GroupFixtures().create_group(name="test name")

        # Act
        result = group_api.get_all_groups_except_list([group])

        # Assert
        self.assertEqual(len(result), 2)
