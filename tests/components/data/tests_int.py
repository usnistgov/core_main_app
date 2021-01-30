""" Unit Test Data
"""
from types import SimpleNamespace

from bson.objectid import ObjectId
import datetime
import pytz
from mock.mock import patch

from core_main_app.commons import exceptions
from core_main_app.components.data.api import check_xml_file_is_valid
from core_main_app.components.data.models import Data
from core_main_app.components.data import api as data_api
from core_main_app.system import api as system_api
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.settings import DATA_SORTING_FIELDS
from tests.components.data.fixtures.fixtures import (
    DataFixtures,
    AccessControlDataFixture,
)
from core_main_app.components.data import tasks as data_task
from core_main_app.components.template import api as template_api
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    MongoIntegrationTransactionTestCase,
)
from tests.components.user.fixtures.fixtures import UserFixtures
from tests.components.data.fixtures.fixtures import DataMigrationFixture

fixture_data_template = DataMigrationFixture()
fixture_data = DataFixtures()
access_control_data_fixture = AccessControlDataFixture()


class TestDataGetAll(MongoIntegrationBaseTestCase):

    fixture = access_control_data_fixture

    def test_data_get_all_return_collection_of_data(self):
        # Act
        result = Data.get_all(DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_return_objects_data_in_collection(self):
        # Act
        result = Data.get_all(DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(len(self.fixture.data_collection) == result.count())

    def test_data_get_all_ordering(self):
        # Arrange
        access_control_data_fixture.insert_data()
        ascending_order_by_field = ["+title"]
        descending_order_by_field = ["-title"]
        # Act
        ascending_result = Data.get_all(ascending_order_by_field)
        descending_result = Data.get_all(descending_order_by_field)
        # Assert
        for i in range(len(ascending_result)):
            self.assertTrue(
                ascending_result.all()[i].title
                == descending_result.all()[len(ascending_result) - i - 1].title
            )

    def test_data_get_all_ascending_sorting(self):
        # Arrange
        ascending_order_by_field = ["+title"]
        # Act
        ascending_result = Data.get_all(ascending_order_by_field)
        # Assert
        self.assertTrue(self.fixture.data_1.title == ascending_result.all()[0].title)
        self.assertTrue(self.fixture.data_2.title == ascending_result.all()[1].title)

    def test_data_get_all_descending_sorting(self):
        # Arrange
        descending_order_by_field = ["-title"]
        # Act
        descending_result = Data.get_all(descending_order_by_field)
        # Assert
        self.assertTrue(
            self.fixture.data_2.title
            == descending_result.all()[len(descending_result) - 2].title
        )
        self.assertTrue(
            self.fixture.data_1.title
            == descending_result.all()[len(descending_result) - 1].title
        )

    def test_data_get_all_multi_field_sorting(self):
        # Arrange
        ascending_order_by_multi_field = ["+title", "+user_id"]
        descending_order_by_multi_field = ["+title", "-user_id"]
        # Act
        ascending_result = Data.get_all(ascending_order_by_multi_field)
        descending_result = Data.get_all(descending_order_by_multi_field)
        # Assert
        self.assertEqual(self.fixture.data_4.user_id, ascending_result.all()[4].user_id)
        self.assertEqual(self.fixture.data_5.user_id, ascending_result.all()[3].user_id)

        self.assertEqual(
            self.fixture.data_4.user_id, descending_result.all()[3].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, descending_result.all()[4].user_id
        )

    def test_data_get_all_api_without_sorting_param_use_default_data_sorting_setting(
        self,
    ):
        # Arrange
        mock_user = _create_user("1", is_superuser=True)
        # Act
        data = data_api.get_all(mock_user)
        # Assert
        self.assertListEqual(list(data), self.fixture.data_collection)


class TestDataGetAllExcept(MongoIntegrationBaseTestCase):

    fixture = access_control_data_fixture

    def test_data_get_all_except_return_collection_of_data(self):
        # Act
        db_content = Data.get_all(DATA_SORTING_FIELDS)
        excluded_id_list = [str(db_content[0].pk)]

        result = Data.get_all_except([], excluded_id_list)
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_return_objects_data_in_collection(self):
        # Act
        db_content = Data.get_all(DATA_SORTING_FIELDS)
        excluded_id_list = [str(db_content[0].pk)]

        result = Data.get_all_except([], excluded_id_list)
        # Assert
        self.assertTrue(
            result.count() == len(self.fixture.data_collection) - len(excluded_id_list)
        )

    def test_data_get_all_except_empty_list_return_collection_of_data(self):
        # Act
        result = Data.get_all_except(DATA_SORTING_FIELDS, id_list=[])
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_except_empty_list_return_objects_data_in_collection(self):
        # Act
        result = Data.get_all_except(DATA_SORTING_FIELDS, id_list=[])
        # Assert
        self.assertTrue(result.count() == len(self.fixture.data_collection))

    def test_data_get_all_except_inexistant_id_return_collection_of_data(self):
        # Act
        object_id_list = [str(data.pk) for data in Data.get_all(DATA_SORTING_FIELDS)]
        inexistant_object_id = str(ObjectId())

        # If the generated object id correspond to one in DB we generate another one
        while inexistant_object_id in object_id_list:
            inexistant_object_id = str(ObjectId)

        excluded_id_list = [inexistant_object_id]

        result = Data.get_all_except([], excluded_id_list)
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_except_inexistant_id_return_objects_data_in_collection(self):
        # Act
        object_id_list = [str(data.pk) for data in Data.get_all(DATA_SORTING_FIELDS)]
        inexistant_object_id = str(ObjectId())

        # If the generated object id correspond to one in DB we generate another one
        while inexistant_object_id in object_id_list:
            inexistant_object_id = str(ObjectId)

        excluded_id_list = [inexistant_object_id]

        result = Data.get_all_except([], excluded_id_list)
        # Assert
        self.assertTrue(result.count() == len(self.fixture.data_collection))

    def test_data_get_all_except_no_params_return_collection_of_data(self):
        # Act
        result = Data.get_all_except(DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_except_no_params_return_objects_data_in_collection(self):
        # Act
        result = Data.get_all_except(DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(result.count() == len(self.fixture.data_collection))

    def test_get_all_except_data_ordering(self):
        # Arrange
        ascending_order_by_field = ["+title"]
        descending_order_by_field = ["-title"]
        # Act
        ascending_result = Data.get_all_except(ascending_order_by_field)
        descending_result = Data.get_all_except(descending_order_by_field)
        # Assert
        for i in range(len(ascending_result)):
            self.assertTrue(
                ascending_result.all()[i].title
                == descending_result.all()[len(ascending_result) - i - 1].title
            )

    def test_get_all_except_data_ascending_sorting(self):
        # Arrange
        ascending_order_by_field = ["+title"]
        # Act
        ascending_result = Data.get_all_except(ascending_order_by_field)
        # Assert
        self.assertTrue(self.fixture.data_1.title == ascending_result.all()[0].title)
        self.assertTrue(self.fixture.data_2.title == ascending_result.all()[1].title)

    def test_get_all_except_data_descending_sorting(self):
        # Arrange
        descending_order_by_field = ["-title"]
        # Act
        descending_result = Data.get_all_except(descending_order_by_field)
        # Assert
        self.assertTrue(
            self.fixture.data_2.title
            == descending_result.all()[len(descending_result) - 2].title
        )
        self.assertTrue(
            self.fixture.data_1.title
            == descending_result.all()[len(descending_result) - 1].title
        )

    def test_get_all_except_data_multi_field_sorting(self):
        # Arrange
        ascending_order_by_multi_field = ["+title", "+user_id"]
        descending_order_by_multi_field = ["+title", "-user_id"]
        # Act
        ascending_result = Data.get_all_except(ascending_order_by_multi_field)
        descending_result = Data.get_all_except(descending_order_by_multi_field)
        # Assert
        self.assertEqual(self.fixture.data_4.user_id, ascending_result.all()[4].user_id)
        self.assertEqual(self.fixture.data_5.user_id, ascending_result.all()[3].user_id)

        self.assertEqual(
            self.fixture.data_4.user_id, descending_result.all()[3].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, descending_result.all()[4].user_id
        )


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

    fixture = access_control_data_fixture

    def test_data_get_all_by_user_id_return_collection_of_data_from_user(self):
        # Arrange
        user_id = 1
        # Act
        result = Data.get_all_by_user_id(user_id, DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(all(item.user_id == str(user_id) for item in result))

    def test_data_get_all_by_user_id_return_empty_collection_of_data_from_user_does_not_exist(
        self,
    ):
        # Arrange
        user_id = 800
        # Act
        result = Data.get_all_by_user_id(user_id, DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(result.count() == 0)

    def test_get_all_by_user_id_data_ordering(self):
        # Arrange
        user_id = 1
        ascending_order_by_field = ["+title"]
        descending_order_by_field = ["-title"]
        # Act
        ascending_result = Data.get_all_by_user_id(user_id, ascending_order_by_field)
        descending_result = Data.get_all_by_user_id(user_id, descending_order_by_field)
        # Assert
        for i in range(len(ascending_result)):
            self.assertTrue(
                ascending_result.all()[i].title
                == descending_result.all()[len(ascending_result) - i - 1].title
            )

    def test_get_all_by_user_id_data_ascending_sorting(self):
        # Arrange
        ascending_order_by_field = ["+title"]
        user_id = 1
        # Act
        ascending_result = Data.get_all_by_user_id(user_id, ascending_order_by_field)
        # Assert
        self.assertTrue(self.fixture.data_1.title == ascending_result.all()[0].title)
        self.assertTrue(self.fixture.data_3.title == ascending_result.all()[1].title)

    def test_get_all_by_user_id_data_descending_sorting(self):
        # Arrange
        descending_order_by_field = ["-title"]
        user_id = 1
        # Act
        descending_result = Data.get_all_by_user_id(user_id, descending_order_by_field)
        # Assert
        self.assertTrue(
            self.fixture.data_3.title
            == descending_result.all()[len(descending_result) - 2].title
        )
        self.assertTrue(
            self.fixture.data_1.title
            == descending_result.all()[len(descending_result) - 1].title
        )

    def test_get_all_by_user_id_multi_field_sorting(self):
        # Arrange
        ascending_order_by_multi_field = ["+user_id", "+title"]
        descending_order_by_multi_field = ["+user_id", "-title"]
        # Act
        ascending_result = Data.get_all_by_user_id(1, ascending_order_by_multi_field)
        descending_result = Data.get_all_by_user_id(1, descending_order_by_multi_field)
        # Assert
        self.assertEqual(self.fixture.data_1.title, ascending_result.all()[0].title)
        self.assertEqual(self.fixture.data_3.title, ascending_result.all()[1].title)

        self.assertEqual(self.fixture.data_3.title, descending_result.all()[1].title)
        self.assertEqual(self.fixture.data_1.title, descending_result.all()[2].title)

    def test_data_get_all_api_without_sorting_param_use_default_data_sorting_setting(
        self,
    ):
        # Arrange
        mock_user = _create_user("1", is_superuser=True)
        # Act
        data = data_api.get_all_by_user(mock_user)
        # Assert
        self.assertListEqual(
            list(data), [self.fixture.data_1, self.fixture.data_3, self.fixture.data_5]
        )


class TestDataGetAllExceptUserId(MongoIntegrationBaseTestCase):

    fixture = access_control_data_fixture

    def test_data_get_all_except_user_id_return_collection_of_data_where_user_is_not_owner(
        self,
    ):
        # Arrange
        user_id = 1
        # Act
        result = Data.get_all_except_user_id(user_id, DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(item.user_id != user_id for item in result)

    def test_data_get_all_by_user_id_return_full_collection_of_data_from_user_does_not_exist(
        self,
    ):
        # Arrange
        user_id = 800
        # Act
        result = Data.get_all_except_user_id(user_id, DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(result.count() > 0)

    def test_get_all_except_user_id_data_ordering(self):
        # Arrange
        user_id = 1
        ascending_order_by_field = ["+title"]
        descending_order_by_field = ["-title"]
        # Act
        ascending_result = Data.get_all_except_user_id(
            user_id, ascending_order_by_field
        )
        descending_result = Data.get_all_except_user_id(
            user_id, descending_order_by_field
        )
        # Assert
        for i in range(len(ascending_result)):
            self.assertTrue(
                ascending_result.all()[i].title
                == descending_result.all()[len(ascending_result) - i - 1].title
            )

    def test_get_all_except_user_id_data_ascending_sorting(self):
        # Arrange
        ascending_order_by_field = ["+title"]
        user_id = 2
        # Act
        ascending_result = Data.get_all_except_user_id(
            user_id, ascending_order_by_field
        )
        # Assert
        self.assertTrue(self.fixture.data_1.title == ascending_result.all()[0].title)
        self.assertTrue(self.fixture.data_3.title == ascending_result.all()[1].title)

    def test_get_all_except_user_id_data_descending_sorting(self):
        # Arrange
        descending_order_by_field = ["-title"]
        user_id = 2
        # Act
        descending_result = Data.get_all_except_user_id(
            user_id, descending_order_by_field
        )
        # Assert
        self.assertTrue(
            self.fixture.data_3.title
            == descending_result.all()[len(descending_result) - 2].title
        )
        self.assertTrue(
            self.fixture.data_1.title
            == descending_result.all()[len(descending_result) - 1].title
        )

    def test_get_all_except_user_id_multi_field_sorting(self):
        # Arrange
        ascending_order_by_multi_field = ["+title", "+user_id"]
        descending_order_by_multi_field = ["+title", "-user_id"]
        # Act
        ascending_result = Data.get_all_except_user_id(
            3, ascending_order_by_multi_field
        )
        descending_result = Data.get_all_except_user_id(
            3, descending_order_by_multi_field
        )
        # Assert
        self.assertEqual(self.fixture.data_4.user_id, ascending_result.all()[4].user_id)
        self.assertEqual(self.fixture.data_5.user_id, ascending_result.all()[3].user_id)

        self.assertEqual(
            self.fixture.data_4.user_id, descending_result.all()[3].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, descending_result.all()[4].user_id
        )

    def test_data_get_all_except_user_api_without_sorting_param_use_default_data_sorting_setting(
        self,
    ):
        # Arrange
        mock_user = _create_user("1", is_superuser=True)
        # Act
        data = data_api.get_all_except_user(mock_user)
        # Assert
        self.assertListEqual(list(data), [self.fixture.data_2, self.fixture.data_4])


class TestExecuteQuery(MongoIntegrationTransactionTestCase):

    fixture = access_control_data_fixture

    def test_execute_query_data_ordering(self):
        # Arrange
        query = {}
        ascending_order_by_field = ["+title"]
        descending_order_by_field = ["-title"]
        # Act
        ascending_result = Data.execute_query(query, ascending_order_by_field)
        descending_result = Data.execute_query(query, descending_order_by_field)
        # Assert
        for i in range(len(ascending_result)):
            self.assertTrue(
                ascending_result.all()[i].title
                == descending_result.all()[len(ascending_result) - i - 1].title
            )

    def test_execute_query_data_ascending_sorting(self):
        # Arrange
        ascending_order_by_field = ["+title"]
        query = {}
        # Act
        ascending_result = Data.execute_query(query, ascending_order_by_field)
        # Assert
        self.assertTrue(self.fixture.data_1.title == ascending_result.all()[0].title)
        self.assertTrue(self.fixture.data_2.title == ascending_result.all()[1].title)

    def test_execute_query_data_descending_sorting(self):
        # Arrange
        descending_order_by_field = ["-title"]
        query = {}
        # Act
        descending_result = Data.execute_query(query, descending_order_by_field)
        # Assert
        self.assertTrue(
            self.fixture.data_2.title
            == descending_result.all()[len(descending_result) - 2].title
        )
        self.assertTrue(
            self.fixture.data_1.title
            == descending_result.all()[len(descending_result) - 1].title
        )

    def test_execute_query_multi_field_sorting(self):
        # Arrange
        ascending_order_by_multi_field = ["+title", "+user_id"]
        descending_order_by_multi_field = ["+title", "-user_id"]
        query = {}
        # Act
        ascending_result = Data.execute_query(query, ascending_order_by_multi_field)
        descending_result = Data.execute_query(query, descending_order_by_multi_field)
        # Assert
        self.assertEqual(self.fixture.data_4.user_id, ascending_result.all()[4].user_id)
        self.assertEqual(self.fixture.data_5.user_id, ascending_result.all()[3].user_id)

        self.assertEqual(
            self.fixture.data_4.user_id, descending_result.all()[3].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, descending_result.all()[4].user_id
        )

    def test_data_execute_query_api_without_sorting_param_use_default_data_sorting_setting(
        self,
    ):
        # Arrange
        mock_user = _create_user("1", is_superuser=True)
        # Act
        data = data_api.execute_query({}, mock_user)
        # Assert
        self.assertListEqual(list(data), self.fixture.data_collection)


class TestGetAllByWorkspace(MongoIntegrationBaseTestCase):

    fixture = access_control_data_fixture

    def test_get_all_by_workspace_data_ordering(self):
        # Arrange
        workspace = self.fixture.workspace_1.id
        ascending_order_by_field = ["+title"]
        descending_order_by_field = ["-title"]
        # Act
        ascending_result = Data.get_all_by_workspace(
            workspace, ascending_order_by_field
        )
        descending_result = Data.get_all_by_workspace(
            workspace, descending_order_by_field
        )
        # Assert
        for i in range(len(ascending_result)):
            self.assertTrue(
                ascending_result.all()[i].title
                == descending_result.all()[len(ascending_result) - i - 1].title
            )

    def test_get_all_by_workspace_data_ascending_sorting(self):
        # Arrange
        ascending_order_by_field = ["+title"]
        workspace = self.fixture.workspace_1.id
        # Act
        ascending_result = Data.get_all_by_workspace(
            workspace, ascending_order_by_field
        )
        # Assert
        self.assertTrue(self.fixture.data_3.title == ascending_result.all()[0].title)
        self.assertTrue(self.fixture.data_5.title == ascending_result.all()[1].title)

    def test_get_all_by_workspace_data_descending_sorting(self):
        # Arrange
        descending_order_by_field = ["-title"]
        workspace = self.fixture.workspace_1.id
        # Act
        descending_result = Data.get_all_by_workspace(
            workspace, descending_order_by_field
        )
        # Assert
        self.assertTrue(
            self.fixture.data_5.title
            == descending_result.all()[len(descending_result) - 2].title
        )
        self.assertTrue(
            self.fixture.data_3.title
            == descending_result.all()[len(descending_result) - 1].title
        )

    def test_get_all_by_workspace_multi_field_sorting(self):
        # Arrange
        ascending_order_by_multi_field = ["+workspace", "+title"]
        descending_order_by_multi_field = ["+workspace", "-title"]
        workspace = self.fixture.workspace_1.id
        # Act
        ascending_result = Data.get_all_by_workspace(
            workspace, ascending_order_by_multi_field
        )
        descending_result = Data.get_all_by_workspace(
            workspace, descending_order_by_multi_field
        )
        # Assert
        self.assertEqual(self.fixture.data_3.user_id, ascending_result.all()[0].user_id)
        self.assertEqual(self.fixture.data_5.user_id, ascending_result.all()[1].user_id)

        self.assertEqual(
            self.fixture.data_3.user_id, descending_result.all()[1].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, descending_result.all()[0].user_id
        )

    def test_data_get_all_by_workspace_api_without_sorting_param_use_default_data_sorting_setting(
        self,
    ):
        # Arrange
        mock_user = _create_user("1", is_superuser=True)
        workspace = self.fixture.workspace_1.id
        # Act
        data = data_api.get_all_by_workspace(workspace, mock_user)
        # Assert
        self.assertListEqual(list(data), [self.fixture.data_3, self.fixture.data_5])


class TestGetAllByListTemplate(MongoIntegrationBaseTestCase):
    fixture = access_control_data_fixture

    def test_returns_data_object(self):
        result = Data.get_all_by_list_workspace(
            [self.fixture.workspace_1.id, self.fixture.workspace_2.id],
            DATA_SORTING_FIELDS,
        )
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_returns_correct_count(self):
        result = Data.get_all_by_list_workspace(
            [self.fixture.workspace_1.id, self.fixture.workspace_2.id],
            DATA_SORTING_FIELDS,
        )
        self.assertEqual(len(result), 3)

    def test_none_returns_data_object(self):
        result = Data.get_all_by_list_workspace([None], DATA_SORTING_FIELDS)
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_none_returns_correct_count(self):
        result = Data.get_all_by_list_workspace([None], DATA_SORTING_FIELDS)
        self.assertEqual(len(result), 2)

    def test_empty_list_returns_no_data(self):
        result = Data.get_all_by_list_workspace([], DATA_SORTING_FIELDS)
        self.assertEqual(len(result), 0)

    def test_invalid_workspace_returns_no_data(self):
        result = Data.get_all_by_list_workspace([ObjectId()], DATA_SORTING_FIELDS)
        self.assertEqual(len(result), 0)


class TestGetAllByTemplatesAndWorkspaces(MongoIntegrationBaseTestCase):
    fixture = access_control_data_fixture

    def test_returns_data_object(self):
        result = Data.get_all_by_templates_and_workspaces(
            [self.fixture.template.id],
            [self.fixture.workspace_1.id, self.fixture.workspace_2.id],
            DATA_SORTING_FIELDS,
        )
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_returns_correct_count(self):
        result = Data.get_all_by_templates_and_workspaces(
            [self.fixture.template.id],
            [self.fixture.workspace_1.id, self.fixture.workspace_2.id],
            DATA_SORTING_FIELDS,
        )
        self.assertEqual(len(result), 3)

    def test_null_workspace_returns_data_object(self):
        result = Data.get_all_by_templates_and_workspaces(
            [self.fixture.template.id], [None], DATA_SORTING_FIELDS
        )
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_null_workspace_returns_correct_count(self):
        result = Data.get_all_by_templates_and_workspaces(
            [self.fixture.template.id], [None], DATA_SORTING_FIELDS
        )
        self.assertEqual(len(result), 2)

    def test_empty_workspaces_returns_no_data(self):
        result = Data.get_all_by_templates_and_workspaces(
            [self.fixture.template.id], [], DATA_SORTING_FIELDS
        )
        self.assertEqual(len(result), 0)

    def test_empty_templates_returns_no_data(self):
        result = Data.get_all_by_templates_and_workspaces(
            [], [None], DATA_SORTING_FIELDS
        )
        self.assertEqual(len(result), 0)

    def test_invalid_workspace_returns_no_data(self):
        result = Data.get_all_by_templates_and_workspaces(
            [self.fixture.template.id], [ObjectId()], DATA_SORTING_FIELDS
        )
        self.assertEqual(len(result), 0)

    def test_invalid_template_returns_no_data(self):
        result = Data.get_all_by_templates_and_workspaces(
            [ObjectId()], [None], DATA_SORTING_FIELDS
        )
        self.assertEqual(len(result), 0)


class TestGetAllByUserAndWorkspace(MongoIntegrationBaseTestCase):

    fixture = access_control_data_fixture

    def test_get_all_data_from_user_and_from_workspace_for_user_within_workspace(self):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=False)
        # Act
        data = Data.get_all_by_user_and_workspace(
            mock_user.id,
            [self.fixture.workspace_1, self.fixture.workspace_2],
            ["+title"],
        )
        # Assert
        self.assertListEqual(
            list(data),
            [
                self.fixture.data_1,
                self.fixture.data_3,
                self.fixture.data_4,
                self.fixture.data_5,
            ],
        )

    def test_get_all_data_from_user_and_from_workspace_data_ordering(self):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=False)
        ascending_order_by_field = ["+title"]
        descending_order_by_field = ["-title"]
        # Act
        ascending_result = Data.get_all_by_user_and_workspace(
            mock_user.id, [self.fixture.workspace_1], ascending_order_by_field
        )
        descending_result = Data.get_all_by_user_and_workspace(
            mock_user.id, [self.fixture.workspace_1], descending_order_by_field
        )
        # Assert
        for i in range(len(ascending_result)):
            self.assertTrue(
                ascending_result.all()[i].title
                == descending_result.all()[len(ascending_result) - i - 1].title
            )

    def test_get_all_data_from_user_and_from_workspace_data_ascending_sorting(self):
        # Arrange
        ascending_order_by_field = ["+title"]
        mock_user = create_mock_user("1", is_superuser=False)
        # Act
        ascending_result = Data.get_all_by_user_and_workspace(
            mock_user.id, [self.fixture.workspace_1], ascending_order_by_field
        )
        # Assert
        self.assertTrue(self.fixture.data_1.title == ascending_result.all()[0].title)
        self.assertTrue(self.fixture.data_3.title == ascending_result.all()[1].title)

    def test_get_all_data_from_user_and_from_workspace_data_descending_sorting(self):
        # Arrange
        descending_order_by_field = ["-title"]
        mock_user = create_mock_user("1", is_superuser=False)
        # Act
        descending_result = Data.get_all_by_user_and_workspace(
            mock_user.id, [self.fixture.workspace_1], descending_order_by_field
        )
        # Assert
        self.assertTrue(
            self.fixture.data_3.title
            == descending_result.all()[len(descending_result) - 2].title
        )
        self.assertTrue(
            self.fixture.data_1.title
            == descending_result.all()[len(descending_result) - 1].title
        )

    def test_get_all_data_from_user_and_from_workspace_multi_field_sorting(self):
        # Arrange
        ascending_order_by_multi_field = ["+template", "+title"]
        descending_order_by_multi_field = ["+template", "-title"]
        mock_user = create_mock_user("1", is_superuser=False)
        # Act
        ascending_result = Data.get_all_by_user_and_workspace(
            mock_user.id, [self.fixture.workspace_1], ascending_order_by_multi_field
        )
        descending_result = Data.get_all_by_user_and_workspace(
            mock_user.id, [self.fixture.workspace_1], descending_order_by_multi_field
        )
        # Assert
        self.assertEqual(self.fixture.data_1.title, ascending_result.all()[0].title)
        self.assertEqual(self.fixture.data_3.user_id, ascending_result.all()[1].user_id)

        self.assertEqual(
            self.fixture.data_3.user_id, descending_result.all()[1].user_id
        )
        self.assertEqual(
            self.fixture.data_1.user_id, descending_result.all()[2].user_id
        )


class TestDataMigration(MongoIntegrationTransactionTestCase):
    fixture = fixture_data_template

    def setUp(self):
        """Insert needed data.

        Returns:

        """
        super().setUp()
        self.fixture.insert_data()

    @patch.object(data_api, "get_by_id")
    @patch.object(template_api, "get")
    def test_data_template_validation_success_for_one_data(
        self, template_get, data_get_by_id
    ):
        # Arrange
        request_user = UserFixtures().create_super_user("admin_test")
        template_get.return_value = self.fixture.template_2
        data_get_by_id.return_value = self.fixture.data_1

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id], self.fixture.template_2.id, request_user.id, False
        )

        # Assert
        expected_result = {"valid": [str(self.fixture.data_1.id)], "wrong": []}
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_validation_success_for_multi_data(
        self, template_get, data_get_by_id
    ):
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_2]
        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_2.id],
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {
            "valid": [str(self.fixture.data_1.id), str(self.fixture.data_2.id)],
            "wrong": [],
        }
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(template_api, "get")
    def test_data_template_validation_error_for_one_data(
        self, template_get, data_get_by_id
    ):
        # Arrange
        data_get_by_id.return_value = self.fixture.data_5
        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_5.id],
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {"valid": [], "wrong": [str(self.fixture.data_5.id)]}
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(template_api, "get")
    def test_data_template_validation_for_multi_data(
        self, template_get, data_get_by_id
    ):
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_5]
        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_5.id],
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {
            "valid": [str(self.fixture.data_1.id)],
            "wrong": [str(self.fixture.data_5.id)],
        }
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "execute_query")
    @patch.object(data_api, "get_by_id")
    @patch.object(template_api, "get")
    def test_data_template_group_validation_success(
        self, template_get, data_get_by_id, data_execute_query
    ):
        # Arrange
        mock_query_set = {
            "values_list": lambda param: [
                self.fixture.data_1.id,
                self.fixture.data_2.id,
            ],
            "count": lambda: 2,
        }
        data_execute_query.return_value = SimpleNamespace(**mock_query_set)
        data_get_by_id.side_effect = [
            self.fixture.data_1,
            self.fixture.data_2,
        ]

        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_template_migration_task(
            [self.fixture.template_1.id],
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {
            "valid": [str(self.fixture.data_1.id), str(self.fixture.data_2.id)],
            "wrong": [],
        }
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "execute_query")
    @patch.object(data_api, "get_by_id")
    @patch.object(template_api, "get")
    def test_data_template_group_validation_error(
        self, template_get, data_get_by_id, data_execute_query
    ):
        # Arrange
        mock_query_set = {
            "values_list": lambda param: [
                self.fixture.data_4.id,
                self.fixture.data_5.id,
            ],
            "count": lambda: 2,
        }
        data_execute_query.return_value = SimpleNamespace(**mock_query_set)
        data_get_by_id.side_effect = [
            self.fixture.data_4,
            self.fixture.data_5,
        ]

        template_get.return_value = self.fixture.template_1
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_template_migration_task(
            [self.fixture.template_3.id],
            self.fixture.template_1.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {
            "valid": [],
            "wrong": [str(self.fixture.data_4.id), str(self.fixture.data_5.id)],
        }
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "upsert")
    @patch.object(template_api, "get")
    def test_data_template_migration_success_for_one_data(
        self, template_get, data_upsert, data_get_by_id
    ):
        # Arrange
        request_user = UserFixtures().create_super_user("admin_test")
        data_upsert.side_effect = mock_upsert
        template_get.return_value = self.fixture.template_2
        data_get_by_id.return_value = self.fixture.data_1

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id], self.fixture.template_2.id, request_user.id, True
        )

        # Assert
        migrated_data = data_api.get_by_id(self.fixture.data_1.id, request_user)
        self.assertEqual(migrated_data.template.id, self.fixture.template_2.id)

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "upsert")
    @patch.object(template_api, "get")
    def test_data_template_migration_success_for_multi_data(
        self, template_get, data_upsert, data_get_by_id
    ):
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_2]
        template_get.return_value = self.fixture.template_2
        data_upsert.side_effect = mock_upsert
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_2.id],
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        migrated_data_template = [
            self.fixture.data_1.template.id,
            self.fixture.data_2.template.id,
        ]
        self.assertListEqual(
            migrated_data_template,
            [self.fixture.template_2.id, self.fixture.template_2.id],
        )

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "upsert")
    @patch.object(template_api, "get")
    def test_data_template_migration_error_for_one_data(
        self, template_get, data_upsert, data_get_by_id
    ):
        # Arrange
        request_user = UserFixtures().create_super_user("admin_test")
        data_upsert.side_effect = mock_upsert
        template_get.return_value = self.fixture.template_2
        data_get_by_id.return_value = self.fixture.data_5

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_5.id], self.fixture.template_2.id, request_user.id, True
        )

        # Assert
        migrated_data = data_api.get_by_id(self.fixture.data_5.id, request_user)
        self.assertEqual(migrated_data.template.id, self.fixture.template_2.id)

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "upsert")
    @patch.object(template_api, "get")
    def test_data_template_migration_for_multi_data(
        self, template_get, data_upsert, data_get_by_id
    ):
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_5]
        template_get.return_value = self.fixture.template_2
        data_upsert.side_effect = mock_upsert
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_5.id],
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        migrated_data_template = [
            self.fixture.data_1.template.id,
            self.fixture.data_5.template.id,
        ]
        self.assertListEqual(
            migrated_data_template,
            [self.fixture.template_2.id, self.fixture.template_2.id],
        )

        @patch.object(data_api, "execute_query")
        @patch.object(template_api, "get")
        def test_data_template_group_migration_success(
            self, template_get, data_execute_query
        ):
            # Arrange
            data_execute_query.return_value = [self.fixture.data_1, self.fixture.data_2]
            template_get.return_value = self.fixture.template_2
            request_user = UserFixtures().create_super_user("admin_test")

            # Act
            response = data_task.async_template_migration_task(
                [self.fixture.template_1.id],
                self.fixture.template_2.id,
                request_user.id,
                True,
            )

            # Assert
            migrated_data_template = [
                self.fixture.data_1.template.id,
                self.fixture.data_2.template.id,
            ]
            self.assertListEqual(
                migrated_data_template,
                [self.fixture.template_2.id, self.fixture.template_2.id],
            )

    @patch.object(data_api, "execute_query")
    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_group_migration_error(
        self, template_get, data_get_by_id, data_execute_query
    ):
        # Arrange
        mock_query_set = {
            "values_list": lambda param: [
                self.fixture.data_4.id,
                self.fixture.data_5.id,
            ],
            "count": lambda: 2,
        }
        data_execute_query.return_value = SimpleNamespace(**mock_query_set)
        data_get_by_id.side_effect = [
            self.fixture.data_4,
            self.fixture.data_5,
        ]

        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_template_migration_task(
            [self.fixture.template_3.id],
            self.fixture.template_1.id,
            request_user.id,
            True,
        )

        # Assert
        migrated_data_template = [
            self.fixture.data_4.template.id,
            self.fixture.data_5.template.id,
        ]
        self.assertListEqual(
            migrated_data_template,
            [self.fixture.template_3.id, self.fixture.template_3.id],
        )


@patch.object(data_api, "get_by_id")
@patch.object(data_api, "upsert")
@patch.object(template_api, "get")
def test_result_data_template_migration_success_for_one_data(
    self, template_get, data_upsert, data_get_by_id
):
    # Arrange
    request_user = UserFixtures().create_super_user("admin_test")
    data_upsert.side_effect = mock_upsert
    template_get.return_value = self.fixture.template_2
    data_get_by_id.return_value = self.fixture.data_1

    # Act
    response = data_task.async_migration_task(
        [self.fixture.data_1.id], self.fixture.template_2.id, request_user.id, True
    )

    # Assert
    expected_result = {"valid": [str(self.fixture.data_1.id)], "wrong": []}
    self.assertEqual(response, expected_result)


@patch.object(data_api, "get_by_id")
@patch.object(data_api, "upsert")
@patch.object(template_api, "get")
def test_result_data_template_migration_success_for_multi_data(
    self, template_get, data_upsert, data_get_by_id
):
    # Arrange
    data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_2]
    template_get.return_value = self.fixture.template_2
    data_upsert.side_effect = mock_upsert
    request_user = UserFixtures().create_super_user("admin_test")

    # Act
    response = data_task.async_migration_task(
        [self.fixture.data_1.id, self.fixture.data_2.id],
        self.fixture.template_2.id,
        request_user.id,
        False,
    )

    # Assert
    expected_result = {
        "valid": [str(self.fixture.data_1.id), str(self.fixture.data_2.id)],
        "wrong": [],
    }
    self.assertEqual(response, expected_result)


@patch.object(data_api, "get_by_id")
@patch.object(data_api, "upsert")
@patch.object(template_api, "get")
def test_result_data_template_migration_error_for_one_data(
    self, template_get, data_upsert, data_get_by_id
):
    # Arrange
    request_user = UserFixtures().create_super_user("admin_test")
    data_upsert.side_effect = mock_upsert
    template_get.return_value = self.fixture.template_2
    data_get_by_id.return_value = self.fixture.data_5

    # Act
    response = data_task.async_migration_task(
        [self.fixture.data_5.id], self.fixture.template_2.id, request_user.id, True
    )

    # Assert
    expected_result = {"valid": [], "wrong": [str(self.fixture.data_5.id)]}
    self.assertEqual(response, expected_result)


@patch.object(data_api, "get_by_id")
@patch.object(data_api, "upsert")
@patch.object(template_api, "get")
def test_result_data_template_migration_for_multi_data(
    self, template_get, data_upsert, data_get_by_id
):
    # Arrange
    data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_5]
    template_get.return_value = self.fixture.template_2
    data_upsert.side_effect = mock_upsert
    request_user = UserFixtures().create_super_user("admin_test")

    # Act
    response = data_task.async_migration_task(
        [self.fixture.data_1.id, self.fixture.data_5.id],
        self.fixture.template_2.id,
        request_user.id,
        False,
    )

    # Assert
    expected_result = {
        "valid": [str(self.fixture.data_1.id)],
        "wrong": [str(self.fixture.data_5.id)],
    }
    self.assertEqual(response, expected_result)

    @patch.object(data_api, "execute_query")
    @patch.object(template_api, "get")
    def test_result_data_template_group_migration_success(
        self, template_get, data_execute_query
    ):
        # Arrange
        data_execute_query.return_value = [self.fixture.data_1, self.fixture.data_2]
        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_template_migration_task(
            [self.fixture.template_1.id],
            self.fixture.template_2.id,
            request_user.id,
            True,
        )

        # Assert
        expected_result = {
            "valid": [str(self.fixture.data_1.id), str(self.fixture.data_2.id)],
            "wrong": [],
        }
        self.assertEqual(response, expected_result)


@patch.object(data_api, "execute_query")
@patch.object(template_api, "get")
def test_result_data_template_group_migration_error(
    self, template_get, data_execute_query
):
    # Arrange
    data_execute_query.return_value = [self.fixture.data_4, self.fixture.data_5]
    template_get.return_value = self.fixture.template_2
    request_user = UserFixtures().create_super_user("admin_test")

    # Act
    response = data_task.async_template_migration_task(
        [self.fixture.template_3.id],
        self.fixture.template_1.id,
        request_user.id,
        True,
    )

    # Assert
    expected_result = {
        "valid": [],
        "wrong": [str(self.fixture.data_4.id), str(self.fixture.data_5.id)],
    }
    self.assertEqual(response, expected_result)


def mock_upsert(data, user):
    if data.xml_content is None:
        raise exceptions.ApiError("Unable to save data: xml_content field is not set.")

    data.last_modification_date = datetime.datetime.now(pytz.utc)
    check_xml_file_is_valid(data)
    return data.save()


def _create_user(user_id, is_superuser=False):
    return create_mock_user(user_id, is_superuser=is_superuser)
