""" Unit Test Data
"""
from core_main_app.utils.integration_tests.integration_base_test_case import MongoIntegrationBaseTestCase
from tests.components.data.fixtures.fixtures import DataFixtures
from core_main_app.components.data.models import Data
from core_main_app.commons import exceptions
from bson.objectid import ObjectId

fixture_data = DataFixtures()


class TestDataGetAll(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_data_get_all_return_collection_of_data(self):
        # Act
        result = Data.get_all()
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_return_objects_data_in_collection(self):
        # Act
        result = Data.get_all()
        # Assert
        self.assertTrue(len(self.fixture.data_collection) == result.count())


class TestDataGetById(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_data_get_by_id_raises_api_error_if_not_found(self):
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            Data.get_by_id(ObjectId())

    def test_data_get_by_id_return_data_if_found(self):
        # Act
        result = Data.get_by_id(self.fixture.data_1.id)
        # Assert
        self.assertEqual(result, self.fixture.data_1)


class TestDataGetAllByUserId(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_data_get_all_by_user_id_return_collection_of_data_from_user(self):
        # Arrange
        user_id = 1
        # Act
        result = Data.get_all_by_user_id(user_id)
        # Assert
        self.assertTrue(all(item.user_id == str(user_id) for item in result))

    def test_data_get_all_by_user_id_return_empty_collection_of_data_from_user_does_not_exist(self):
        # Arrange
        user_id = 800
        # Act
        result = Data.get_all_by_user_id(user_id)
        # Assert
        self.assertTrue(result.count() == 0)


class TestDataGetAllExceptUserId(MongoIntegrationBaseTestCase):

    fixture = fixture_data

    def test_data_get_all_except_user_id_return_collection_of_data_where_user_is_not_owner(self):
        # Arrange
        user_id = 1
        # Act
        result = Data.get_all_except_user_id(user_id)
        # Assert
        self.assertTrue(item.user_id != user_id for item in result)

    def test_data_get_all_by_user_id_return_full_collection_of_data_from_user_does_not_exist(self):
        # Arrange
        user_id = 800
        # Act
        result = Data.get_all_except_user_id(user_id)
        # Assert
        self.assertTrue(result.count() > 0)
