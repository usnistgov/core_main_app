""" Access control testing
"""
import unittest

from mock.mock import patch

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.components.data.fixtures.fixtures import AccessControlDataFixture

fixture_data = AccessControlDataFixture()


class TestDataGetById(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_by_id_owner_with_read_access_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        data_id = self.fixture.data_collection[fixture_data.USER_1_WORKSPACE_1].id
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data = data_api.get_by_id(data_id, mock_user)
        self.assertTrue(isinstance(data, Data))

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_by_id_owner_without_read_access_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        data_id = self.fixture.data_collection[fixture_data.USER_1_WORKSPACE_1].id
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.get_by_id(data_id, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_by_id_owner_without_read_access_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        data_id = self.fixture.data_collection[fixture_data.USER_1_WORKSPACE_1].id
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        data = data_api.get_by_id(data_id, mock_user)
        self.assertTrue(isinstance(data, Data))

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_by_id_user_without_read_access_raises_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        data_id = self.fixture.data_collection[fixture_data.USER_1_WORKSPACE_1].id
        mock_user = _create_user("2")
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.get_by_id(data_id, mock_user)

    def test_get_by_id_owner_no_workspace_read_access_returns_data(self):
        data_id = self.fixture.data_collection[fixture_data.USER_1_NO_WORKSPACE].id
        mock_user = _create_user("1")
        data = data_api.get_by_id(data_id, mock_user)
        self.assertTrue(isinstance(data, Data))

    def test_get_by_id_not_owner_no_workspace_raises_error(self):
        data_id = self.fixture.data_collection[fixture_data.USER_1_NO_WORKSPACE].id
        mock_user = _create_user("2")
        with self.assertRaises(AccessControlError):
            data_api.get_by_id(data_id, mock_user)


class TestDataGetAll(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_get_all_as_superuser_returns_all_data(self):
        mock_user = _create_user("1", is_superuser=True)
        data_list = data_api.get_all(mock_user)
        self.assertTrue(len(data_list) == len(self.fixture.data_collection))

    def test_get_all_as_user_raises_error(self):
        mock_user = _create_user("1")
        with self.assertRaises(AccessControlError):
            data_api.get_all(mock_user)


class TestDataGetAllByUser(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_returns_data(self, get_all_workspaces_with_read_access_by_user):
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.get_all_except_user(mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_by_user_returns_owned_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        mock_user = _create_user("1")
        data_list = data_api.get_all_by_user(mock_user)
        get_all_workspaces_with_read_access_by_user.return_value = []
        self.assertTrue(len(data_list) == 3)
        self.assertTrue(data.id == "1" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_by_user_returns_no_data_if_owns_zero(
        self, get_all_workspaces_with_read_access_by_user
    ):
        mock_user = _create_user("3")
        data_list = data_api.get_all_by_user(mock_user)
        get_all_workspaces_with_read_access_by_user.return_value = []
        self.assertTrue(len(data_list) == 0)

    def test_get_all_by_user_as_superuser_returns_own_data(self):
        mock_user = _create_user("1", is_superuser=True)
        data_list = data_api.get_all_by_user(mock_user)
        self.assertTrue(len(data_list) == 3)
        self.assertTrue(data.user_id == "1" for data in data_list)


class TestDataGetAllExceptUser(MongoIntegrationBaseTestCase):
    # NOTE: Will always fail when private data are present (data.workspace=None, data.user_id!=user.id)
    fixture = fixture_data

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_except_user_raises_error_if_no_workspace_access(
        self, get_all_workspaces_with_read_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.get_all_except_user(mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_except_user_raises_error_data_if_workspace_access(
        self, get_all_workspaces_with_read_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1,
            fixture_data.workspace_2,
        ]
        with self.assertRaises(AccessControlError):
            data_api.get_all_except_user(mock_user)

    def test_get_all_except_user_as_superuser_returns_others_data(self):
        mock_user = _create_user("1", is_superuser=True)
        data_list = data_api.get_all_except_user(mock_user)
        self.assertTrue(len(data_list) > 0)
        self.assertTrue(data.user_id != mock_user.id for data in data_list)


class TestDataUpsert(MongoIntegrationBaseTestCase):
    # TODO: can not test without mock for GridFS
    pass


class TestDataExecuteQuery(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        mock_user = _create_user("3")
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data_list = data_api.execute_query({}, mock_user)
        self.assertTrue(len(data_list) > 0)
        self.assertTrue(all(isinstance(data, Data) for data in data_list))

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_returns_data_in_workspace_1(
        self, get_all_workspaces_with_read_access_by_user
    ):
        mock_user = _create_user("3")
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data_list = data_api.execute_query({}, mock_user)
        self.assertTrue(len(data_list) == 2)
        self.assertTrue(data.workspace == "1" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_returns_data_in_workspace_2(
        self, get_all_workspaces_with_read_access_by_user
    ):
        mock_user = _create_user("3")
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data_list = data_api.execute_query({}, mock_user)
        self.assertTrue(len(data_list) == 2)
        self.assertTrue(data.workspace == "2" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_returns_data_in_workspace_1_and_2(
        self, get_all_workspaces_with_read_access_by_user
    ):
        mock_user = _create_user("3")
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1,
            fixture_data.workspace_2,
        ]
        data_list = data_api.execute_query({}, mock_user)
        self.assertTrue(len(data_list) == 3)
        self.assertTrue(
            data.workspace == "1" or data.workspace == "2" for data in data_list
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_force_workspace_1_returns_data_from_workspace_1(
        self, get_all_workspaces_with_read_access_by_user
    ):
        mock_user = _create_user("3")
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data_list = data_api.execute_query(
            {"workspace": fixture_data.workspace_1.id}, mock_user
        )
        self.assertTrue(len(data_list) == 2)
        self.assertTrue(data.workspace == "1" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_force_workspace_1_does_not_return_data_if_no_access(
        self, get_all_workspaces_with_read_access_by_user
    ):
        mock_user = _create_user("3")
        get_all_workspaces_with_read_access_by_user.return_value = []
        data_list = data_api.execute_query(
            {"workspace": fixture_data.workspace_1.id}, mock_user
        )
        self.assertTrue(len(data_list) == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_force_workspace_none_does_not_return_data_if_no_access(
        self, get_all_workspaces_with_read_access_by_user
    ):
        mock_user = _create_user("3")
        get_all_workspaces_with_read_access_by_user.return_value = []
        data_list = data_api.execute_query({"workspace": None}, mock_user)
        self.assertTrue(len(data_list) == 0)

    def test_execute_query_as_superuser_returns_all_data(self):
        mock_user = _create_user("1", is_superuser=True)
        data_list = data_api.execute_query({}, mock_user)
        self.assertTrue(len(data_list) == 5)


class TestDataDelete(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    @unittest.skip("GridFS not supported by mongomock")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_data_in_accessible_workspace_deletes_data(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data_api.delete(
            fixture_data.data_collection[fixture_data.USER_1_WORKSPACE_1], mock_user
        )

    @unittest.skip("GridFS not supported by mongomock")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_data_in_not_accessible_workspace_deletes_data(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = []
        data_api.delete(
            fixture_data.data_collection[fixture_data.USER_1_WORKSPACE_1], mock_user
        )

    @unittest.skip("GridFS not supported by mongomock")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_others_data_in_accessible_workspace_deletes_data(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_data.workspace_2
        ]
        data_api.delete(
            fixture_data.data_collection[fixture_data.USER_2_WORKSPACE_2], mock_user
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_others_data_not_accessible_workspace_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        with self.assertRaises(AccessControlError):
            data_api.delete(
                fixture_data.data_collection[fixture_data.USER_2_WORKSPACE_2], mock_user
            )

    @unittest.skip("GridFS not supported by mongomock")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_data_not_in_workspace_deletes_data(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.delete(
                fixture_data.data_collection[fixture_data.USER_1_WORKSPACE_1], mock_user
            )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_others_data_not_in_workspace_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.delete(
                fixture_data.data_collection[fixture_data.USER_2_NO_WORKSPACE],
                mock_user,
            )


class TestDataChangeOwner(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_change_owner_from_owner_to_owner_ok(self):
        mock_owner = _create_user("1")
        data_api.change_owner(
            document=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
            new_user=mock_owner,
            user=mock_owner,
        )

    def test_change_owner_from_owner_to_user_ok(self):
        mock_owner = _create_user("1")
        mock_user = _create_user("2")
        data_api.change_owner(
            document=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
            new_user=mock_user,
            user=mock_owner,
        )

    def test_change_owner_from_user_to_user_raises_exception(self):
        mock_owner = _create_user("1")
        mock_user = _create_user("2")
        with self.assertRaises(AccessControlError):
            data_api.change_owner(
                document=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
                new_user=mock_owner,
                user=mock_user,
            )

    def test_change_owner_as_superuser_ok(self):
        mock_user = _create_user("2", is_superuser=True)
        data_api.change_owner(
            document=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
            new_user=mock_user,
            user=mock_user,
        )


def _create_user(user_id, is_superuser=False):
    return create_mock_user(user_id, is_superuser=is_superuser)
