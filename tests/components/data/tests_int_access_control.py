""" Access control testing
"""
from core_main_app.components.data.models import Data
from core_main_app.components.data import api as data_api

from core_main_app.components.data.tests.fixtures.fixtures import AccessControlDataFixture
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.integration_tests.integration_base_test_case import MongoIntegrationBaseTestCase
from core_main_app.utils.tests_tools.MockUser import MockUser

import unittest

fixture_data = AccessControlDataFixture()


class TestDataGetById(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_get_by_id_as_owner_returns_data(self):
        data_id = self.fixture.data_collection[fixture_data.USER_1_NO_WORKSPACE].id
        mock_user = _create_user('1')
        data = data_api.get_by_id(data_id, mock_user)
        self.assertEquals(data.user_id, mock_user.id)

    def test_get_by_id_not_owner_returns_data(self):
        data_id = self.fixture.data_collection[fixture_data.USER_1_NO_WORKSPACE].id
        mock_user = _create_user('2')
        data = data_api.get_by_id(data_id, mock_user)
        self.assertTrue(isinstance(data, Data))

    def test_get_by_id_data_in_workspace_as_owner_returns_data(self):
        data_id = self.fixture.data_collection[fixture_data.USER_1_WORKSPACE_1].id
        mock_user = _create_user('1')
        data = data_api.get_by_id(data_id, mock_user)
        self.assertEquals(data.user_id, mock_user.id)

    def test_get_by_id_data_in_workspace_not_owner_returns_data(self):
        data_id = self.fixture.data_collection[fixture_data.USER_2_WORKSPACE_2].id
        mock_user = _create_user('2')
        data = data_api.get_by_id(data_id, mock_user)
        self.assertTrue(isinstance(data, Data))

    def test_get_by_id_not_owner_as_superuser_returns_data(self):
        data_id = self.fixture.data_collection[fixture_data.USER_1_NO_WORKSPACE].id
        mock_user = _create_user('2', is_superuser=True)
        data = data_api.get_by_id(data_id, mock_user)
        self.assertTrue(isinstance(data, Data))


class TestDataGetAll(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_get_all_returns_data(self):
        mock_user = _create_user('1')
        data_list = data_api.get_all(mock_user)
        self.assertTrue(isinstance(data, Data) for data in data_list)

    def test_get_all_returns_owned_data(self):
        mock_user = _create_user('1')
        data_list = data_api.get_all(mock_user)
        self.assertTrue(data.id == '1' for data in data_list)

    def test_get_all_returns_no_data_if_owns_zero(self):
        mock_user = _create_user('3')
        data_list = data_api.get_all(mock_user)
        self.assertTrue(data_list.count() == 0)

    def test_get_all_as_superuser_returns_own_data(self):
        mock_user = _create_user('1', is_superuser=True)
        data_list = data_api.get_all(mock_user)
        self.assertTrue(data_list.count() == 2)
        self.assertTrue(data.user_id == '1' for data in data_list)


class TestDataGetAllExceptUser(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_get_all_except_user_returns_data(self):
        mock_user = _create_user('1')
        data_list = data_api.get_all_except_user(mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(isinstance(data, Data) for data in data_list)

    def test_get_all_except_user_returns_others_data(self):
        mock_user = _create_user('1')
        data_list = data_api.get_all_except_user(mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(data.user_id != mock_user.id for data in data_list)

    def test_get_all_except_user_returns_all_data_if_owns_zero(self):
        mock_user = _create_user('3')
        data_list = data_api.get_all_except_user(mock_user)
        self.assertTrue(data_list.count() == 4)

    def test_get_all_except_user_as_superuser_returns_others_data(self):
        mock_user = _create_user('1', is_superuser=True)
        data_list = data_api.get_all_except_user(mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(data.user_id != mock_user.id for data in data_list)


class TestDataUpsert(MongoIntegrationBaseTestCase):

    # TODO: can not test without mock for GridFS
    fixture = fixture_data

    @unittest.skip("GridFS not supported by mongomock")
    def test_upsert_update_title_own_data(self):
        mock_user = _create_user('1')
        data = fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE]
        data.title = "test"
        data_api.upsert(data, mock_user)
        self.assertEqual(data.title, "test")

    @unittest.skip("GridFS not supported by mongomock")
    def test_upsert_update_title_others_data(self):
        mock_user = _create_user('1')
        data = fixture_data.data_collection[fixture_data.USER_2_NO_WORKSPACE]
        data.title = "test"
        with self.assertRaises(AccessControlError):
            data_api.upsert(data, mock_user)


class TestDataExecuteQuery(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_execute_query_returns_data(self):
        mock_user = _create_user('1')
        data_list = data_api.execute_query({}, mock_user)
        self.assertTrue(isinstance(data, Data) for data in data_list)

    def test_execute_query_returns_all_data(self):
        mock_user = _create_user('1')
        data_list = data_api.execute_query({}, mock_user)
        self.assertTrue(data_list.count() == 4)

    def test_execute_query_returns_other_users_data(self):
        mock_user = _create_user('1')
        data_list = data_api.execute_query({'user_id': '2'}, mock_user)
        self.assertTrue(data_list.count() == 2)
        self.assertTrue(data.user_id == '2' for data in data_list)

    def test_execute_query_as_superuser_returns_all_data(self):
        mock_user = _create_user('1', is_superuser=True)
        data_list = data_api.execute_query({}, mock_user)
        self.assertTrue(data_list.count() == 4)


class TestDataDelete(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    @unittest.skip("GridFS not supported by mongomock")
    def test_delete_own_data_deletes_data(self):
        mock_user = _create_user('1')
        data_api.delete(fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE], mock_user)

    def test_delete_others_data_raises_error(self):
        mock_user = _create_user('1')
        with self.assertRaises(AccessControlError):
            data_api.delete(fixture_data.data_collection[fixture_data.USER_2_NO_WORKSPACE], mock_user)


class TestDataChangeOwner(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_change_owner_from_owner_to_owner_ok(self):
        mock_owner = _create_user('1')
        data_api.change_owner(data=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
                              new_user=mock_owner,
                              user=mock_owner)

    def test_change_owner_from_owner_to_user_ok(self):
        mock_owner = _create_user('1')
        mock_user = _create_user('2')
        data_api.change_owner(data=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
                              new_user=mock_user,
                              user=mock_owner)

    def test_change_owner_from_user_to_user_raises_exception(self):
        mock_owner = _create_user('1')
        mock_user = _create_user('2')
        with self.assertRaises(AccessControlError):
            data_api.change_owner(data=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
                                  new_user=mock_owner,
                                  user=mock_user)

    def test_change_owner_as_superuser_ok(self):
        mock_user = _create_user('2', is_superuser=True)
        data_api.change_owner(data=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
                              new_user=mock_user,
                              user=mock_user)


def _create_user(user_id, is_superuser=False):
    return MockUser(user_id, is_superuser=is_superuser)
