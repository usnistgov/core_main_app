""" Unit Test Data
"""
from core_main_app.components.data.models import Data
from core_main_app.commons import exceptions
from core_main_app.utils.mongo_integration_test_base import IntegrationTest
from bson.objectid import ObjectId


class TestDataGetAll(IntegrationTest):

    def setUp(self):
        # Make a connexion with a mock database
        super(TestDataGetAll, self).setUp()
        # Arrange the scenario for TestDataAll test methods
        super(TestDataGetAll, self).insert_two_data()

    def test_data_get_all_return_collection_of_data(self):
        # Act
        result = Data.get_all()
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_return_two_objects_data_in_collection(self):
        # Act
        result = Data.get_all()
        # Assert
        self.assertTrue(2 == len(result))


class TestDataGetById(IntegrationTest):

    def setUp(self):
        # Make a connexion with a mock database
        super(TestDataGetById, self).setUp()
        # Arrange the scenario for TestDataAll test methods
        super(TestDataGetById, self).insert_two_data()

    def test_data_get_by_id_raises_api_error_if_not_found(self):
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            Data.get_by_id(ObjectId())

    def test_data_get_by_id_return_data_if_found(self):
        # Act
        result = Data.get_by_id(self.data_1.id)
        # Assert
        self.assertEqual(result, self.data_1)


class TestDataGetAllByUser(IntegrationTest):

    def setUp(self):
        # Make a connexion with a mock database
        super(TestDataGetAllByUser, self).setUp()
        # Arrange the scenario for TestDataAll test methods
        super(TestDataGetAllByUser, self).insert_two_data()

    def test_data_get_all_by_user_return_collection_of_data_from_user(self):
        # Arrange
        user_id = 1
        # Act
        result = Data.get_all_by_user_id(user_id)
        # Assert
        self.assertTrue(all(item.user_id == str(user_id) for item in result))


class TestDataGetAllExceptUser(IntegrationTest):

    def setUp(self):
        # Make a connexion with a mock database
        super(TestDataGetAllExceptUser, self).setUp()
        # Arrange the scenario for TestDataAll test methods
        super(TestDataGetAllExceptUser, self).insert_two_data()

    def test_data_get_all_except_user_return_collection_of_data_where_user_is_not_owner(self):
        # Arrange
        user_id = 1
        # Act
        result = Data.get_all_except_user_id(user_id)
        # Assert
        self.assertTrue(all(item.user_id != user_id for item in result))
