""" Integration tests Data
"""

from types import SimpleNamespace
from unittest.mock import patch

from django.db.models import Q
from tests.components.data.fixtures.fixtures import (
    DataFixtures,
    AccessControlDataFixture,
)
from tests.components.data.fixtures.fixtures import DataMigrationFixture
from tests.components.user.fixtures.fixtures import UserFixtures

from core_main_app.commons import exceptions
from core_main_app.components.data import api as data_api
from core_main_app.components.data import tasks as data_task
from core_main_app.components.data.api import check_xml_file_is_valid
from core_main_app.components.data.models import Data
from core_main_app.settings import DATA_SORTING_FIELDS
from core_main_app.system import api as system_api
from core_main_app.utils.datetime import datetime_now
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user

fixture_data_template = DataMigrationFixture()
fixture_data = DataFixtures()
access_control_data_fixture = AccessControlDataFixture()


class TestDataGetAll(IntegrationBaseTestCase):
    """TestDataGetAll"""

    fixture = access_control_data_fixture

    def test_data_get_all_return_collection_of_data(self):
        """test_data_get_all_return_collection_of_data

        Returns:

        """
        # Act
        result = Data.get_all(DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_return_objects_data_in_collection(self):
        """test_data_get_all_return_objects_data_in_collection

        Returns:

        """
        # Act
        result = Data.get_all(DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(len(self.fixture.data_collection) == result.count())

    def test_data_get_all_ordering(self):
        """test_data_get_all_ordering

        Returns:

        """
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
        """test_data_get_all_ascending_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_field = ["+title"]
        # Act
        ascending_result = Data.get_all(ascending_order_by_field)
        # Assert
        self.assertTrue(
            self.fixture.data_1.title == ascending_result.all()[0].title
        )
        self.assertTrue(
            self.fixture.data_2.title == ascending_result.all()[1].title
        )

    def test_data_get_all_descending_sorting(self):
        """test_data_get_all_descending_sorting

        Returns:

        """
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
        """test_data_get_all_multi_field_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_multi_field = ["+title", "+user_id"]
        descending_order_by_multi_field = ["+title", "-user_id"]
        # Act
        ascending_result = Data.get_all(ascending_order_by_multi_field)
        descending_result = Data.get_all(descending_order_by_multi_field)
        # Assert
        self.assertEqual(
            self.fixture.data_4.user_id, ascending_result.all()[4].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, ascending_result.all()[3].user_id
        )

        self.assertEqual(
            self.fixture.data_4.user_id, descending_result.all()[3].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, descending_result.all()[4].user_id
        )

    def test_data_get_all_api_without_sorting_param_use_default_data_sorting_setting(
        self,
    ):
        """test_data_get_all_api_without_sorting_param_use_default_data_sorting_setting

        Returns:

        """
        # Arrange
        mock_user = _create_user("1", is_superuser=True)
        # Act
        queryset = data_api.get_all(mock_user)
        # Assert
        self.assertListEqual(
            [data.title for data in list(queryset)],
            [data.title for data in self.fixture.data_collection],
        )


class TestDataGetAllExcept(IntegrationBaseTestCase):
    """TestDataGetAllExcept"""

    fixture = access_control_data_fixture

    def test_data_get_all_except_return_collection_of_data(self):
        """test_data_get_all_except_return_collection_of_data

        Returns:

        """
        # Act
        db_content = Data.get_all(DATA_SORTING_FIELDS)
        excluded_id_list = [str(db_content[0].pk)]

        result = Data.get_all_except([], excluded_id_list)
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_return_objects_data_in_collection(self):
        """test_data_get_all_return_objects_data_in_collection

        Returns:

        """
        # Act
        db_content = Data.get_all(DATA_SORTING_FIELDS)
        excluded_id_list = [str(db_content[0].pk)]

        result = Data.get_all_except([], excluded_id_list)
        # Assert
        self.assertTrue(
            result.count()
            == len(self.fixture.data_collection) - len(excluded_id_list)
        )

    def test_data_get_all_except_empty_list_return_collection_of_data(self):
        """test_data_get_all_except_empty_list_return_collection_of_data

        Returns:

        """
        # Act
        result = Data.get_all_except(DATA_SORTING_FIELDS, id_list=[])
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_except_empty_list_return_objects_data_in_collection(
        self,
    ):
        """test_data_get_all_except_empty_list_return_objects_data_in_collection

        Returns:

        """
        # Act
        result = Data.get_all_except(DATA_SORTING_FIELDS, id_list=[])
        # Assert
        self.assertTrue(result.count() == len(self.fixture.data_collection))

    def test_data_get_all_except_nonexistent_id_return_collection_of_data(
        self,
    ):
        """test_data_get_all_except_nonexistent_id_return_collection_of_data

        Returns:

        """
        # Act
        nonexistent_object_id = -1

        excluded_id_list = [nonexistent_object_id]

        result = Data.get_all_except([], excluded_id_list)
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_except_nonexistent_id_return_objects_data_in_collection(
        self,
    ):
        """test_data_get_all_except_nonexistent_id_return_objects_data_in_collection

        Returns:

        """
        # Act
        nonexistent_object_id = -1

        excluded_id_list = [nonexistent_object_id]

        result = Data.get_all_except([], excluded_id_list)
        # Assert
        self.assertTrue(result.count() == len(self.fixture.data_collection))

    def test_data_get_all_except_no_params_return_collection_of_data(self):
        """test_data_get_all_except_no_params_return_collection_of_data

        Returns:

        """
        # Act
        result = Data.get_all_except(DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    def test_data_get_all_except_no_params_return_objects_data_in_collection(
        self,
    ):
        """test_data_get_all_except_no_params_return_objects_data_in_collection

        Returns:

        """
        # Act
        result = Data.get_all_except(DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(result.count() == len(self.fixture.data_collection))

    def test_get_all_except_data_ordering(self):
        """test_get_all_except_data_ordering

        Returns:

        """
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
        """test_get_all_except_data_ascending_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_field = ["+title"]
        # Act
        ascending_result = Data.get_all_except(ascending_order_by_field)
        # Assert
        self.assertTrue(
            self.fixture.data_1.title == ascending_result.all()[0].title
        )
        self.assertTrue(
            self.fixture.data_2.title == ascending_result.all()[1].title
        )

    def test_get_all_except_data_descending_sorting(self):
        """test_get_all_except_data_descending_sorting

        Returns:

        """
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
        """test_get_all_except_data_multi_field_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_multi_field = ["+title", "+user_id"]
        descending_order_by_multi_field = ["+title", "-user_id"]
        # Act
        ascending_result = Data.get_all_except(ascending_order_by_multi_field)
        descending_result = Data.get_all_except(
            descending_order_by_multi_field
        )
        # Assert
        self.assertEqual(
            self.fixture.data_4.user_id, ascending_result.all()[4].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, ascending_result.all()[3].user_id
        )

        self.assertEqual(
            self.fixture.data_4.user_id, descending_result.all()[3].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, descending_result.all()[4].user_id
        )


class TestDataGetById(IntegrationBaseTestCase):
    """TestDataGetById"""

    fixture = fixture_data

    def test_data_get_by_id_raises_api_error_if_not_found(self):
        """test_data_get_by_id_raises_api_error_if_not_found

        Returns:

        """
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            Data.get_by_id(-1)

    def test_data_get_by_id_return_data_if_found(self):
        """test_data_get_by_id_return_data_if_found

        Returns:

        """
        # Act
        result = Data.get_by_id(self.fixture.data_1.id)
        # Assert
        self.assertEqual(result, self.fixture.data_1)


class TestDataGetAllByUserId(IntegrationBaseTestCase):
    """TestDataGetAllByUserId"""

    fixture = access_control_data_fixture

    def test_data_get_all_by_user_id_return_collection_of_data_from_user(self):
        """test_data_get_all_by_user_id_return_collection_of_data_from_user

        Returns:

        """
        # Arrange
        user_id = 1
        # Act
        result = Data.get_all_by_user_id(user_id, DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(all(item.user_id == str(user_id) for item in result))

    def test_data_get_all_by_user_id_return_empty_collection_of_data_from_user_does_not_exist(
        self,
    ):
        """test_data_get_all_by_user_id_return_empty_collection_of_data_from_user_does_not_exist

        Returns:

        """
        # Arrange
        user_id = 800
        # Act
        result = Data.get_all_by_user_id(user_id, DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(result.count() == 0)

    def test_get_all_by_user_id_data_ordering(self):
        """test_get_all_by_user_id_data_ordering

        Returns:

        """
        # Arrange
        user_id = 1
        ascending_order_by_field = ["+title"]
        descending_order_by_field = ["-title"]
        # Act
        ascending_result = Data.get_all_by_user_id(
            user_id, ascending_order_by_field
        )
        descending_result = Data.get_all_by_user_id(
            user_id, descending_order_by_field
        )
        # Assert
        for i in range(len(ascending_result)):
            self.assertTrue(
                ascending_result.all()[i].title
                == descending_result.all()[len(ascending_result) - i - 1].title
            )

    def test_get_all_by_user_id_data_ascending_sorting(self):
        """test_get_all_by_user_id_data_ascending_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_field = ["+title"]
        user_id = 1
        # Act
        ascending_result = Data.get_all_by_user_id(
            user_id, ascending_order_by_field
        )
        # Assert
        self.assertTrue(
            self.fixture.data_1.title == ascending_result.all()[0].title
        )
        self.assertTrue(
            self.fixture.data_3.title == ascending_result.all()[1].title
        )

    def test_get_all_by_user_id_data_descending_sorting(self):
        """test_get_all_by_user_id_data_descending_sorting

        Returns:

        """
        # Arrange
        descending_order_by_field = ["-title"]
        user_id = 1
        # Act
        descending_result = Data.get_all_by_user_id(
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

    def test_get_all_by_user_id_multi_field_sorting(self):
        """test_get_all_by_user_id_multi_field_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_multi_field = ["+user_id", "+title"]
        descending_order_by_multi_field = ["+user_id", "-title"]
        # Act
        ascending_result = Data.get_all_by_user_id(
            1, ascending_order_by_multi_field
        )
        descending_result = Data.get_all_by_user_id(
            1, descending_order_by_multi_field
        )
        # Assert
        self.assertEqual(
            self.fixture.data_1.title, ascending_result.all()[0].title
        )
        self.assertEqual(
            self.fixture.data_3.title, ascending_result.all()[1].title
        )

        self.assertEqual(
            self.fixture.data_3.title, descending_result.all()[1].title
        )
        self.assertEqual(
            self.fixture.data_1.title, descending_result.all()[2].title
        )

    def test_data_get_all_api_without_sorting_param_use_default_data_sorting_setting(
        self,
    ):
        """test_data_get_all_api_without_sorting_param_use_default_data_sorting_setting

        Returns:

        """
        # Arrange
        mock_user = _create_user("1", is_superuser=True)
        # Act
        data = data_api.get_all_by_user(mock_user)
        # Assert
        self.assertListEqual(
            list(data),
            [self.fixture.data_1, self.fixture.data_3, self.fixture.data_5],
        )


class TestDataGetAllExceptUserId(IntegrationBaseTestCase):
    """TestDataGetAllExceptUserId"""

    fixture = access_control_data_fixture

    def test_data_get_all_except_user_id_return_collection_of_data_where_user_is_not_owner(
        self,
    ):
        """test_data_get_all_except_user_id_return_collection_of_data_where_user_is_not_owner

        Returns:

        """
        # Arrange
        user_id = 1
        # Act
        result = Data.get_all_except_user_id(user_id, DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(item.user_id != user_id for item in result)

    def test_data_get_all_by_user_id_return_full_collection_of_data_from_user_does_not_exist(
        self,
    ):
        """test_data_get_all_by_user_id_return_full_collection_of_data_from_user_does_not_exist

        Returns:

        """
        # Arrange
        user_id = 800
        # Act
        result = Data.get_all_except_user_id(user_id, DATA_SORTING_FIELDS)
        # Assert
        self.assertTrue(result.count() > 0)

    def test_get_all_except_user_id_data_ordering(self):
        """test_get_all_except_user_id_data_ordering

        Returns:

        """
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
        """test_get_all_except_user_id_data_ascending_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_field = ["+title"]
        user_id = 2
        # Act
        ascending_result = Data.get_all_except_user_id(
            user_id, ascending_order_by_field
        )
        # Assert
        self.assertTrue(
            self.fixture.data_1.title == ascending_result.all()[0].title
        )
        self.assertTrue(
            self.fixture.data_3.title == ascending_result.all()[1].title
        )

    def test_get_all_except_user_id_data_descending_sorting(self):
        """test_get_all_except_user_id_data_descending_sorting

        Returns:

        """
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
        """test_get_all_except_user_id_multi_field_sorting

        Returns:

        """
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
        self.assertEqual(
            self.fixture.data_4.user_id, ascending_result.all()[4].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, ascending_result.all()[3].user_id
        )

        self.assertEqual(
            self.fixture.data_4.user_id, descending_result.all()[3].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, descending_result.all()[4].user_id
        )

    def test_data_get_all_except_user_api_without_sorting_param_use_default_data_sorting_setting(
        self,
    ):
        """test_data_get_all_except_user_api_without_sorting_param_use_default_data_sorting_setting

        Returns:

        """
        # Arrange
        mock_user = _create_user("1", is_superuser=True)
        # Act
        data = data_api.get_all_except_user(mock_user)
        # Assert
        self.assertListEqual(
            list(data), [self.fixture.data_2, self.fixture.data_4]
        )


class TestExecuteQuery(IntegrationTransactionTestCase):
    """TestExecuteQuery"""

    fixture = access_control_data_fixture

    def test_execute_query_data_ordering(self):
        """test_execute_query_data_ordering

        Returns:

        """
        # Arrange
        query = Q()
        ascending_order_by_field = ["+title"]
        descending_order_by_field = ["-title"]
        # Act
        ascending_result = Data.execute_query(query, ascending_order_by_field)
        descending_result = Data.execute_query(
            query, descending_order_by_field
        )
        # Assert
        for i in range(len(ascending_result)):
            self.assertTrue(
                ascending_result.all()[i].title
                == descending_result.all()[len(ascending_result) - i - 1].title
            )

    def test_execute_query_data_ascending_sorting(self):
        """test_execute_query_data_ascending_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_field = ["+title"]
        query = Q()
        # Act
        ascending_result = Data.execute_query(query, ascending_order_by_field)
        # Assert
        self.assertTrue(
            self.fixture.data_1.title == ascending_result.all()[0].title
        )
        self.assertTrue(
            self.fixture.data_2.title == ascending_result.all()[1].title
        )

    def test_execute_query_data_descending_sorting(self):
        """test_execute_query_data_descending_sorting

        Returns:

        """
        # Arrange
        descending_order_by_field = ["-title"]
        query = Q()
        # Act
        descending_result = Data.execute_query(
            query, descending_order_by_field
        )
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
        """test_execute_query_multi_field_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_multi_field = ["+title", "+user_id"]
        descending_order_by_multi_field = ["+title", "-user_id"]
        query = Q()
        # Act
        ascending_result = Data.execute_query(
            query, ascending_order_by_multi_field
        )
        descending_result = Data.execute_query(
            query, descending_order_by_multi_field
        )
        # Assert
        self.assertEqual(
            self.fixture.data_4.user_id, ascending_result.all()[4].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, ascending_result.all()[3].user_id
        )

        self.assertEqual(
            self.fixture.data_4.user_id, descending_result.all()[3].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, descending_result.all()[4].user_id
        )

    def test_data_execute_query_api_without_sorting_param_use_default_data_sorting_setting(
        self,
    ):
        """test_data_execute_query_api_without_sorting_param_use_default_data_sorting_setting

        Returns:

        """
        # Arrange
        mock_user = _create_user("1", is_superuser=True)
        # Act
        queryset = data_api.execute_query(Q(), mock_user)
        # Assert
        self.assertListEqual(
            [data.title for data in list(queryset)],
            [data.title for data in self.fixture.data_collection],
        )


class TestGetAllByWorkspace(IntegrationBaseTestCase):
    """TestGetAllByWorkspace"""

    fixture = access_control_data_fixture

    def test_get_all_by_workspace_data_ordering(self):
        """test_get_all_by_workspace_data_ordering

        Returns:

        """
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
        """test_get_all_by_workspace_data_ascending_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_field = ["+title"]
        workspace = self.fixture.workspace_1.id
        # Act
        ascending_result = Data.get_all_by_workspace(
            workspace, ascending_order_by_field
        )
        # Assert
        self.assertTrue(
            self.fixture.data_3.title == ascending_result.all()[0].title
        )
        self.assertTrue(
            self.fixture.data_5.title == ascending_result.all()[1].title
        )

    def test_get_all_by_workspace_data_descending_sorting(self):
        """test_get_all_by_workspace_data_descending_sorting

        Returns:

        """
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
        """test_get_all_by_workspace_multi_field_sorting

        Returns:

        """
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
        self.assertEqual(
            self.fixture.data_3.user_id, ascending_result.all()[0].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, ascending_result.all()[1].user_id
        )

        self.assertEqual(
            self.fixture.data_3.user_id, descending_result.all()[1].user_id
        )
        self.assertEqual(
            self.fixture.data_5.user_id, descending_result.all()[0].user_id
        )

    def test_data_get_all_by_workspace_api_without_sorting_param_use_default_data_sorting_setting(
        self,
    ):
        """test_data_get_all_by_workspace_api_without_sorting_param_use_default_data_sorting_setting

        Returns:

        """
        # Arrange
        mock_user = _create_user("1", is_superuser=True)
        workspace = self.fixture.workspace_1.id
        # Act
        data = data_api.get_all_by_workspace(workspace, mock_user)
        # Assert
        self.assertListEqual(
            list(data), [self.fixture.data_3, self.fixture.data_5]
        )


class TestGetByIdList(IntegrationBaseTestCase):
    """TestGetByIdList"""

    fixture = access_control_data_fixture

    def setUp(self):
        """setUp

        Returns:

        """
        self.user = create_mock_user(1, is_superuser=True)

    @patch.object(Data, "get_all_by_id_list")
    def test_get_by_id_list_returns_data_object(self, mock_get_all_by_id_list):
        """test_get_by_id_list_returns_list_data_object

        Returns:

        """
        mock_get_all_by_id_list.return_value = [
            self.fixture.data_1,
            self.fixture.data_3,
        ]
        result = data_api.get_by_id_list(
            [self.fixture.data_1.id, self.fixture.data_3.id], self.user
        )
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch.object(Data, "get_all_by_id_list")
    def test_get_by_id_list_returns_correct_count(
        self, mock_get_all_by_id_list
    ):
        """test_get_by_id_list_returns_correct_count

        Returns:

        """
        mock_get_all_by_id_list.return_value = [
            self.fixture.data_1,
            self.fixture.data_3,
        ]
        result = data_api.get_by_id_list(
            [self.fixture.data_1.id, self.fixture.data_3.id], self.user
        )
        self.assertEqual(len(result), 2)

    def test_get_by_id_list_none_returns_empty_list(self):
        """test_get_by_id_list_none_returns_empty_list

        Returns:

        """
        result = data_api.get_by_id_list([None], self.user)
        self.assertEqual(len(result), 0)

    def test_get_by_id_list_empty_returns_empty_list(self):
        """test_get_by_id_list_empty_returns_empty_list

        Returns:

        """
        result = data_api.get_by_id_list([], self.user)
        self.assertEqual(len(result), 0)

    def test_get_by_id_list_invalid_id_returns_empty_list(self):
        """test_get_by_id_list_invalid_id_returns_empty_list

        Returns:

        """
        result = data_api.get_by_id_list([-1], self.user)
        self.assertEqual(len(result), 0)


class TestDataMigration(IntegrationTransactionTestCase):
    """TestDataMigration"""

    fixture = fixture_data_template

    def setUp(self):
        """Insert needed data.

        Returns:

        """
        super().setUp()
        self.fixture.insert_data()
        self.fixture.generate_xslt()

    @patch("core_main_app.components.user.api.get_user_by_id")
    def test_validation_as_regular_user_raises_error(self, user_get_by_id):
        """test_validation_as_regular_user_raises_error

        Args:

        Returns:

        """
        # Arrange
        request_user = create_mock_user("2")
        user_get_by_id.return_value = request_user

        # Act
        with self.assertRaises(Exception):
            data_task.async_migration_task(
                [self.fixture.data_1.id],
                None,
                self.fixture.template_2.id,
                request_user.id,
                False,
            )

    @patch("core_main_app.components.user.api.get_user_by_id")
    def test_template_validation_as_regular_user_raises_error(
        self, user_get_by_id
    ):
        """test_template_validation_as_regular_user_raises_error

        Args:

        Returns:

        """
        # Arrange
        request_user = create_mock_user("2")
        user_get_by_id.return_value = request_user

        # Act
        with self.assertRaises(Exception):
            data_task.async_template_migration_task(
                [self.fixture.data_1.id],
                None,
                self.fixture.template_2.id,
                request_user.id,
                False,
            )

    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_validation_success_for_one_data(
        self, template_get, data_get_by_id
    ):
        """test_data_template_validation_success_for_one_data

        Args:
            template_get:
            data_get_by_id:

        Returns:

        """
        # Arrange
        request_user = UserFixtures().create_super_user("admin_test")
        template_get.return_value = self.fixture.template_2
        data_get_by_id.return_value = self.fixture.data_1

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id],
            None,
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {"valid": [str(self.fixture.data_1.id)], "wrong": []}
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_validation_success_for_one_transformed_data(
        self,
        template_get,
        data_get_by_id,
    ):
        """test_data_template_validation_success_for_one_transformed_data

        Args:
            template_get:
            data_get_by_id:

        Returns:

        """
        # Arrange
        request_user = UserFixtures().create_super_user("admin_test")
        template_get.return_value = self.fixture.template_4
        data_get_by_id.return_value = self.fixture.data_1

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id],
            self.fixture.xsl_transformation.id,
            self.fixture.template_4.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {"valid": [str(self.fixture.data_1.id)], "wrong": []}
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_validation_success_for_multi_data(
        self, template_get, data_get_by_id
    ):
        """test_data_template_validation_success_for_multi_data

        Args:
            template_get:
            data_get_by_id:

        Returns:

        """
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_2]
        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_2.id],
            None,
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {
            "valid": [
                str(self.fixture.data_1.id),
                str(self.fixture.data_2.id),
            ],
            "wrong": [],
        }
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_validation_success_for_multi_transformed_data(
        self,
        template_get,
        data_get_by_id,
    ):
        """test_data_template_validation_success_for_multi_transformed_data

        Args:
            template_get:
            data_get_by_id:

        Returns:

        """
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_2]
        template_get.return_value = self.fixture.template_4
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_2.id],
            self.fixture.xsl_transformation.id,
            self.fixture.template_4.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {
            "valid": [
                str(self.fixture.data_1.id),
                str(self.fixture.data_2.id),
            ],
            "wrong": [],
        }
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_validation_error_for_one_data(
        self, template_get, data_get_by_id
    ):
        """test_data_template_validation_error_for_one_data

        Args:
            template_get:
            data_get_by_id:

        Returns:

        """
        # Arrange
        data_get_by_id.return_value = self.fixture.data_5
        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_5.id],
            None,
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {"valid": [], "wrong": [str(self.fixture.data_5.id)]}
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_validation_error_for_one_transformed_data(
        self, template_get, data_get_by_id
    ):
        """test_data_template_validation_error_for_one_transformed_data

        Args:
            template_get:
            data_get_by_id:

        Returns:

        """
        # Arrange
        data_get_by_id.return_value = self.fixture.data_5
        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_5.id],
            self.fixture.xsl_transformation.id,
            self.fixture.template_4.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {"valid": [], "wrong": [str(self.fixture.data_5.id)]}
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_validation_for_multi_data(
        self, template_get, data_get_by_id
    ):
        """test_data_template_validation_for_multi_data

        Args:
            template_get:
            data_get_by_id:

        Returns:

        """
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_5]
        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_5.id],
            None,
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

    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_validation_for_multi_transformed_data(
        self, template_get, data_get_by_id
    ):
        """test_data_template_validation_for_multi_transformed_data

        Args:
            template_get:
            data_get_by_id:

        Returns:

        """
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_5]
        template_get.return_value = self.fixture.template_4
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_5.id],
            self.fixture.xsl_transformation.id,
            self.fixture.template_4.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {
            "valid": [str(self.fixture.data_1.id)],
            "wrong": [str(self.fixture.data_5.id)],
        }
        self.assertEqual(response, expected_result)

    @patch.object(system_api, "get_all_by_template")
    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_group_validation_success(
        self, template_get, data_get_by_id, system_get_all_by_template
    ):
        """test_data_template_group_validation_success

        Args:
            template_get:
            data_get_by_id:
            system_get_all_by_template:

        Returns:

        """
        # Arrange
        mock_query_set = {
            "all": lambda: [
                self.fixture.data_1,
                self.fixture.data_2,
            ],
            "count": lambda: 2,
        }
        system_get_all_by_template.return_value = SimpleNamespace(
            **mock_query_set
        )
        data_get_by_id.side_effect = [
            self.fixture.data_1,
            self.fixture.data_2,
        ]

        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_template_migration_task(
            [self.fixture.template_1.id],
            None,
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {
            "valid": [
                str(self.fixture.data_1.id),
                str(self.fixture.data_2.id),
            ],
            "wrong": [],
        }
        self.assertEqual(response, expected_result)

    @patch.object(system_api, "get_all_by_template")
    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_group_validation_success_with_transformation(
        self, template_get, data_get_by_id, system_get_all_by_template
    ):
        """test_data_template_group_validation_success_with_transformation

        Args:
            template_get:
            data_get_by_id:
            system_get_all_by_template:

        Returns:

        """
        # Arrange
        mock_query_set = {
            "all": lambda: [
                self.fixture.data_1,
                self.fixture.data_2,
            ],
            "count": lambda: 2,
        }
        system_get_all_by_template.return_value = SimpleNamespace(
            **mock_query_set
        )
        data_get_by_id.side_effect = [
            self.fixture.data_1,
            self.fixture.data_2,
        ]

        template_get.return_value = self.fixture.template_4
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_template_migration_task(
            [self.fixture.template_1.id],
            self.fixture.xsl_transformation.id,
            self.fixture.template_4.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {
            "valid": [
                str(self.fixture.data_1.id),
                str(self.fixture.data_2.id),
            ],
            "wrong": [],
        }
        self.assertEqual(response, expected_result)

    @patch.object(system_api, "get_all_by_template")
    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_group_validation_error(
        self, template_get, data_get_by_id, system_get_all_by_template
    ):
        """test_data_template_group_validation_error

        Args:
            template_get:
            data_get_by_id:
            system_get_all_by_template:

        Returns:

        """
        # Arrange
        mock_query_set = {
            "all": lambda: [
                self.fixture.data_4,
                self.fixture.data_5,
            ],
            "count": lambda: 2,
        }
        system_get_all_by_template.return_value = SimpleNamespace(
            **mock_query_set
        )
        data_get_by_id.side_effect = [
            self.fixture.data_4,
            self.fixture.data_5,
        ]

        template_get.return_value = self.fixture.template_1
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_template_migration_task(
            [self.fixture.template_3.id],
            None,
            self.fixture.template_1.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {
            "valid": [],
            "wrong": [
                str(self.fixture.data_4.id),
                str(self.fixture.data_5.id),
            ],
        }
        self.assertEqual(response, expected_result)

    @patch.object(system_api, "get_all_by_template")
    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_group_validation_error_with_transformation(
        self, template_get, data_get_by_id, system_get_all_by_template
    ):
        """test_data_template_group_validation_error_with_transformation

        Args:
            template_get:
            data_get_by_id:
            system_get_all_by_template:

        Returns:

        """
        # Arrange
        mock_query_set = {
            "all": lambda: [
                self.fixture.data_4,
                self.fixture.data_5,
            ],
            "count": lambda: 2,
        }
        system_get_all_by_template.return_value = SimpleNamespace(
            **mock_query_set
        )
        data_get_by_id.side_effect = [
            self.fixture.data_4,
            self.fixture.data_5,
        ]

        template_get.return_value = self.fixture.template_4
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_template_migration_task(
            [self.fixture.template_3.id],
            self.fixture.xsl_transformation.id,
            self.fixture.template_1.id,
            request_user.id,
            False,
        )

        # Assert
        expected_result = {
            "valid": [],
            "wrong": [
                str(self.fixture.data_4.id),
                str(self.fixture.data_5.id),
            ],
        }
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "upsert")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_migration_success_for_one_transformed_data(
        self, template_get, data_upsert, data_get_by_id
    ):
        """test_data_template_migration_success_for_one_transformed_data

        Args:
            template_get:
            data_upsert:
            data_get_by_id:

        Returns:

        """
        # Arrange
        request_user = UserFixtures().create_super_user("admin_test")
        data_upsert.side_effect = mock_upsert
        template_get.return_value = self.fixture.template_4
        data_get_by_id.return_value = self.fixture.data_1

        # Act
        data_task.async_migration_task(
            [self.fixture.data_1.id],
            self.fixture.xsl_transformation.id,
            self.fixture.template_4.id,
            request_user.id,
            True,
        )

        # Assert
        migrated_data = data_api.get_by_id(
            self.fixture.data_1.id, request_user
        )
        self.assertEqual(migrated_data.template.id, self.fixture.template_4.id)

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "upsert")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_migration_success_for_multi_data(
        self, template_get, data_upsert, data_get_by_id
    ):
        """test_data_template_migration_success_for_multi_data

        Args:
            template_get:
            data_upsert:
            data_get_by_id:

        Returns:

        """
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_2]
        template_get.return_value = self.fixture.template_2
        data_upsert.side_effect = mock_upsert
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_2.id],
            None,
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
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_migration_success_for_multi_transformed_data(
        self, template_get, data_upsert, data_get_by_id
    ):
        """test_data_template_migration_success_for_multi_transformed_data

        Args:
            template_get:
            data_upsert:
            data_get_by_id:

        Returns:

        """
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_2]
        template_get.return_value = self.fixture.template_4
        data_upsert.side_effect = mock_upsert
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_2.id],
            self.fixture.xsl_transformation.id,
            self.fixture.template_4.id,
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
            [self.fixture.template_4.id, self.fixture.template_4.id],
        )

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "upsert")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_migration_error_for_one_data(
        self, template_get, data_upsert, data_get_by_id
    ):
        """test_data_template_migration_error_for_one_data

        Args:
            template_get:
            data_upsert:
            data_get_by_id:

        Returns:

        """
        # Arrange
        request_user = UserFixtures().create_super_user("admin_test")
        data_upsert.side_effect = mock_upsert
        template_get.return_value = self.fixture.template_4
        data_get_by_id.return_value = self.fixture.data_5

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_5.id],
            None,
            self.fixture.template_4.id,
            request_user.id,
            True,
        )

        # Assert
        expected_result = {"valid": [], "wrong": [str(self.fixture.data_5.id)]}
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "upsert")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_migration_error_for_one_transformed_data(
        self, template_get, data_upsert, data_get_by_id
    ):
        """test_data_template_migration_error_for_one_transformed_data

        Args:
            template_get:
            data_upsert:
            data_get_by_id:

        Returns:

        """
        # Arrange
        request_user = UserFixtures().create_super_user("admin_test")
        data_upsert.side_effect = mock_upsert
        template_get.return_value = self.fixture.template_4
        data_get_by_id.return_value = self.fixture.data_5

        # Act
        response = data_task.async_migration_task(
            [self.fixture.data_5.id],
            self.fixture.xsl_transformation.id,
            self.fixture.template_4.id,
            request_user.id,
            True,
        )

        # Assert
        expected_result = {"valid": [], "wrong": [str(self.fixture.data_5.id)]}
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "upsert")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_migration_for_multi_data(
        self, template_get, data_upsert, data_get_by_id
    ):
        """test_data_template_migration_for_multi_data

        Args:
            template_get:
            data_upsert:
            data_get_by_id:

        Returns:

        """
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_5]
        template_get.return_value = self.fixture.template_2
        data_upsert.side_effect = mock_upsert
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_5.id],
            None,
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

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "upsert")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_migration_for_multi_transformed_data(
        self, template_get, data_upsert, data_get_by_id
    ):
        """test_data_template_migration_for_multi_transformed_data

        Args:
            template_get:
            data_upsert:
            data_get_by_id:

        Returns:

        """
        # Arrange
        data_get_by_id.side_effect = [self.fixture.data_1, self.fixture.data_5]
        template_get.return_value = self.fixture.template_4
        data_upsert.side_effect = mock_upsert
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        data_task.async_migration_task(
            [self.fixture.data_1.id, self.fixture.data_5.id],
            self.fixture.xsl_transformation.id,
            self.fixture.template_4.id,
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
            [self.fixture.template_4.id, self.fixture.template_4.id],
        )

        @patch.object(system_api, "get_all_by_template")
        @patch.object(system_api, "get_template_by_id")
        def test_data_template_group_migration_success(
            self, template_get, system_get_all_by_template
        ):
            """test_data_template_group_migration_success

            Args:
                self:
                template_get:
                system_get_all_by_template:

            Returns:

            """
            # Arrange
            system_get_all_by_template.return_value = [
                self.fixture.data_1,
                self.fixture.data_2,
            ]
            template_get.return_value = self.fixture.template_2
            request_user = UserFixtures().create_super_user("admin_test")

            # Act
            data_task.async_template_migration_task(
                [self.fixture.template_1.id],
                None,
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

    @patch.object(system_api, "get_all_by_template")
    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_group_migration_error(
        self, template_get, data_get_by_id, system_get_all_by_template
    ):
        """test_data_template_group_migration_error

        Args:
            template_get:
            data_get_by_id:
            system_get_all_by_template:

        Returns:

        """
        # Arrange
        mock_query_set = {
            "all": lambda: [
                self.fixture.data_4,
                self.fixture.data_5,
            ],
            "count": lambda: 2,
        }
        system_get_all_by_template.return_value = SimpleNamespace(
            **mock_query_set
        )
        data_get_by_id.side_effect = [
            self.fixture.data_4,
            self.fixture.data_5,
        ]

        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_template_migration_task(
            [self.fixture.template_3.id],
            None,
            self.fixture.template_1.id,
            request_user.id,
            True,
        )

        # Assert
        expected_result = {
            "valid": [],
            "wrong": [
                str(self.fixture.data_4.id),
                str(self.fixture.data_5.id),
            ],
        }
        self.assertEqual(response, expected_result)

    @patch.object(system_api, "get_all_by_template")
    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_data_template_group_migration_error_with_transformation(
        self, template_get, data_get_by_id, system_get_all_by_template
    ):
        """test_data_template_group_migration_error_with_transformation

        Args:
            template_get:
            data_get_by_id:
            system_get_all_by_template:

        Returns:

        """
        # Arrange
        mock_query_set = {
            "all": lambda: [
                self.fixture.data_4,
                self.fixture.data_5,
            ],
            "count": lambda: 2,
        }
        system_get_all_by_template.return_value = SimpleNamespace(
            **mock_query_set
        )
        data_get_by_id.side_effect = [
            self.fixture.data_4,
            self.fixture.data_5,
        ]

        template_get.return_value = self.fixture.template_4
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        response = data_task.async_template_migration_task(
            [self.fixture.template_3.id],
            self.fixture.xsl_transformation.id,
            self.fixture.template_4.id,
            request_user.id,
            True,
        )

        # Assert
        expected_result = {
            "valid": [],
            "wrong": [
                str(self.fixture.data_4.id),
                str(self.fixture.data_5.id),
            ],
        }
        self.assertEqual(response, expected_result)
        expected_result = {
            "valid": [],
            "wrong": [
                str(self.fixture.data_4.id),
                str(self.fixture.data_5.id),
            ],
        }
        self.assertEqual(response, expected_result)

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(data_api, "check_json_file_is_valid")
    @patch.object(system_api, "get_template_by_id")
    def test_data_xsd_template_validation_call_xml_validation(
        self,
        template_get,
        mock_check_json_file_is_valid,
        mock_check_xml_file_is_valid,
        data_get_by_id,
    ):
        """test_data_xsd_template_validation_call_xml_validation

        Args:
            template_get:
            mock_check_json_file_is_valid
            mock_check_xml_file_is_valid:
            data_get_by_id:

        Returns:

        """
        # Arrange
        request_user = UserFixtures().create_super_user("admin_test")
        template_get.return_value = self.fixture.template_2
        data_get_by_id.return_value = self.fixture.data_1

        # Act
        data_task.async_migration_task(
            [self.fixture.data_1.id],
            None,
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        self.assertTrue(mock_check_xml_file_is_valid.called)
        self.assertFalse(mock_check_json_file_is_valid.called)

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(data_api, "check_json_file_is_valid")
    @patch.object(system_api, "get_template_by_id")
    def test_data_json_template_validation_call_xml_validation(
        self,
        template_get,
        mock_check_json_file_is_valid,
        mock_check_xml_file_is_valid,
        data_get_by_id,
    ):
        """test_data_json_template_validation_call_xml_validation

        Args:
            template_get:
            mock_check_json_file_is_valid:
            mock_check_xml_file_is_valid
            data_get_by_id:

        Returns:

        """
        # Arrange
        request_user = UserFixtures().create_super_user("admin_test")
        self.fixture.template_2.format = "JSON"
        template_get.return_value = self.fixture.template_2
        data_get_by_id.return_value = self.fixture.data_1

        # Act
        data_task.async_migration_task(
            [self.fixture.data_1.id],
            None,
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        self.assertTrue(mock_check_json_file_is_valid.called)
        self.assertFalse(mock_check_xml_file_is_valid.called)

    @patch.object(data_api, "get_by_id")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(data_api, "check_json_file_is_valid")
    @patch.object(system_api, "get_template_by_id")
    def test_data_unknown_template_format_validation_raises_error(
        self,
        template_get,
        mock_check_json_file_is_valid,
        mock_check_xml_file_is_valid,
        data_get_by_id,
    ):
        """test_data_unknown_template_format_validation_raises_error

        Args:
            template_get:
            mock_check_json_file_is_valid:
            mock_check_xml_file_is_valid:
            data_get_by_id:

        Returns:

        """
        # Arrange
        request_user = UserFixtures().create_super_user("admin_test")
        self.fixture.template_2.format = "UNKNOWN"
        template_get.return_value = self.fixture.template_2
        data_get_by_id.return_value = self.fixture.data_1

        # Act
        data_task.async_migration_task(
            [self.fixture.data_1.id],
            None,
            self.fixture.template_2.id,
            request_user.id,
            False,
        )

        # Assert
        self.assertFalse(mock_check_xml_file_is_valid.called)
        self.assertFalse(mock_check_json_file_is_valid.called)

    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(data_api, "check_json_file_is_valid")
    @patch.object(system_api, "get_all_by_template")
    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_xsd_template_migration_calls_xml_validation(
        self,
        template_get,
        data_get_by_id,
        system_get_all_by_template,
        mock_check_json_file_is_valid,
        mock_check_xml_file_is_valid,
    ):
        """test_xsd_template_migration_calls_xml_validation

        Args:
            template_get:
            data_get_by_id:
            system_get_all_by_template:
            mock_check_json_file_is_valid:
            mock_check_xml_file_is_valid:

        Returns:

        """
        # Arrange
        mock_query_set = {
            "all": lambda: [
                self.fixture.data_1,
                self.fixture.data_2,
            ],
            "count": lambda: 2,
        }
        system_get_all_by_template.return_value = SimpleNamespace(
            **mock_query_set
        )
        data_get_by_id.side_effect = [
            self.fixture.data_1,
            self.fixture.data_2,
        ]

        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        data_task.async_template_migration_task(
            [self.fixture.template_1.id],
            None,
            self.fixture.template_2.id,
            request_user.id,
            False,
        )
        # Assert
        self.assertTrue(mock_check_xml_file_is_valid.called)
        self.assertFalse(mock_check_json_file_is_valid.called)

    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(data_api, "check_json_file_is_valid")
    @patch.object(system_api, "get_all_by_template")
    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_json_template_migration_calls_json_validation(
        self,
        template_get,
        data_get_by_id,
        system_get_all_by_template,
        mock_check_json_file_is_valid,
        mock_check_xml_file_is_valid,
    ):
        """test_json_template_migration_calls_json_validation

        Args:
            template_get:
            data_get_by_id:
            system_get_all_by_template:
            mock_check_json_file_is_valid:
            mock_check_xml_file_is_valid:

        Returns:

        """
        # Arrange
        mock_query_set = {
            "all": lambda: [
                self.fixture.data_1,
                self.fixture.data_2,
            ],
            "count": lambda: 2,
        }
        system_get_all_by_template.return_value = SimpleNamespace(
            **mock_query_set
        )
        data_get_by_id.side_effect = [
            self.fixture.data_1,
            self.fixture.data_2,
        ]

        self.fixture.template_2.format = "JSON"
        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        data_task.async_template_migration_task(
            [self.fixture.template_1.id],
            None,
            self.fixture.template_2.id,
            request_user.id,
            False,
        )
        # Assert
        self.assertFalse(mock_check_xml_file_is_valid.called)
        self.assertTrue(mock_check_json_file_is_valid.called)

    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(data_api, "check_json_file_is_valid")
    @patch.object(system_api, "get_all_by_template")
    @patch.object(data_api, "get_by_id")
    @patch.object(system_api, "get_template_by_id")
    def test_unknown_template_format_migration_raises_error(
        self,
        template_get,
        data_get_by_id,
        system_get_all_by_template,
        mock_check_json_file_is_valid,
        mock_check_xml_file_is_valid,
    ):
        """test_unknown_template_format_migration_raises_error

        Args:
            template_get:
            data_get_by_id:
            system_get_all_by_template:
            mock_check_json_file_is_valid:
            mock_check_xml_file_is_valid:

        Returns:

        """
        # Arrange
        mock_query_set = {
            "all": lambda: [
                self.fixture.data_1,
                self.fixture.data_2,
            ],
            "count": lambda: 2,
        }
        system_get_all_by_template.return_value = SimpleNamespace(
            **mock_query_set
        )
        data_get_by_id.side_effect = [
            self.fixture.data_1,
            self.fixture.data_2,
        ]

        self.fixture.template_2.format = "UNKNOWN"
        template_get.return_value = self.fixture.template_2
        request_user = UserFixtures().create_super_user("admin_test")

        # Act
        data_task.async_template_migration_task(
            [self.fixture.template_1.id],
            None,
            self.fixture.template_2.id,
            request_user.id,
            False,
        )
        # Assert
        self.assertFalse(mock_check_xml_file_is_valid.called)
        self.assertFalse(mock_check_json_file_is_valid.called)


def mock_upsert(data, user):
    """mock_upsert

    Args:
        data:
        user:

    Returns:

    """
    if data.xml_content is None:
        raise exceptions.ApiError(
            "Unable to save data: xml_content field is not set."
        )

    data.last_modification_date = datetime_now()
    check_xml_file_is_valid(data)
    return data.save()


def _create_user(user_id, is_superuser=False):
    """_create_user

    Args:
        user_id:
        is_superuser:

    Returns:

    """
    return create_mock_user(user_id, is_superuser=is_superuser)
