""" Access control testing
"""
import re
import unittest

from mock.mock import patch
from tests.components.data.fixtures.fixtures import (
    AccessControlDataFixture,
    AccessControlDataFixture2,
    AccessControlDataFullTextSearchFixture,
)

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request

fixture_data = AccessControlDataFixture()
fixture_data2 = AccessControlDataFixture2()
fixture_data_full_text = AccessControlDataFullTextSearchFixture()


class TestDataGetById(MongoIntegrationBaseTestCase):
    """TestDataGetById"""

    fixture = fixture_data

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_by_id_owner_with_read_access_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test get by id owner with read access returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        data_id = self.fixture.data_collection[fixture_data.USER_1_WORKSPACE_1].id
        mock_user = _create_user(1)
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
        """test get by id owner without read access returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        data_id = self.fixture.data_collection[fixture_data.USER_1_WORKSPACE_1].id
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        data = data_api.get_by_id(data_id, mock_user)
        self.assertTrue(isinstance(data, Data))

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_by_id_user_without_read_access_raises_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test get by id user without read access raises error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        data_id = self.fixture.data_collection[fixture_data.USER_1_WORKSPACE_1].id
        mock_user = _create_user(2)
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.get_by_id(data_id, mock_user)

    def test_get_by_id_owner_no_workspace_read_access_returns_data(self):
        """test get by id owner no workspace read access returns data

        Returns:

        """
        data_id = self.fixture.data_collection[fixture_data.USER_1_NO_WORKSPACE].id
        mock_user = _create_user(1)
        data = data_api.get_by_id(data_id, mock_user)
        self.assertTrue(isinstance(data, Data))

    def test_get_by_id_not_owner_no_workspace_raises_error(self):
        """test get by id not owner no workspace raises error

        Returns:

        """
        data_id = self.fixture.data_collection[fixture_data.USER_1_NO_WORKSPACE].id
        mock_user = _create_user(2)
        with self.assertRaises(AccessControlError):
            data_api.get_by_id(data_id, mock_user)


class TestDataGetAll(MongoIntegrationBaseTestCase):
    """TestDataGetAll"""

    fixture = fixture_data

    def test_get_all_as_superuser_returns_all_data(self):
        """test get all as superuser returns all data

        Returns:

        """
        mock_user = _create_user(1, is_superuser=True)
        data_list = data_api.get_all(mock_user)
        self.assertTrue(len(data_list) == len(self.fixture.data_collection))

    def test_get_all_as_user_raises_error(self):
        """test get all as user raises error

        Returns:

        """
        mock_user = _create_user(1)
        with self.assertRaises(AccessControlError):
            data_api.get_all(mock_user)


class TestDataGetAllByUser(MongoIntegrationBaseTestCase):
    """TestDataGetAllByUser"""

    fixture = fixture_data

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_returns_data(self, get_all_workspaces_with_read_access_by_user):
        """test get all returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.get_all_except_user(mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_by_user_returns_owned_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test get all by user returns owned data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
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
        """test get all by user returns no data if owns zero

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        data_list = data_api.get_all_by_user(mock_user)
        get_all_workspaces_with_read_access_by_user.return_value = []
        self.assertTrue(len(data_list) == 0)

    def test_get_all_by_user_as_superuser_returns_own_data(self):
        """test get all by user as superuser returns own data

        Returns:

        """
        mock_user = _create_user(1, is_superuser=True)
        data_list = data_api.get_all_by_user(mock_user)
        self.assertTrue(len(data_list) == 3)
        self.assertTrue(data.user_id == "1" for data in data_list)


class TestDataGetAllExceptUser(MongoIntegrationBaseTestCase):
    """TestDataGetAllExceptUser"""

    # NOTE: Will always fail when private data are present
    # (data.workspace=None, data.user_id!=user.id)
    fixture = fixture_data

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_except_user_raises_error_if_no_workspace_access(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test get all except user raises error if no workspace access

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.get_all_except_user(mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_except_user_raises_error_data_if_workspace_access(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test get all except user raises error data if workspace access

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1,
            fixture_data.workspace_2,
        ]
        with self.assertRaises(AccessControlError):
            data_api.get_all_except_user(mock_user)

    def test_get_all_except_user_as_superuser_returns_others_data(self):
        """test get all except user as superuser returns others data

        Returns:

        """
        mock_user = _create_user(1, is_superuser=True)
        data_list = data_api.get_all_except_user(mock_user)
        self.assertTrue(len(data_list) > 0)
        self.assertTrue(data.user_id != mock_user.id for data in data_list)


class TestDataUpsert(MongoIntegrationBaseTestCase):
    """TestDataUpsert"""

    fixture = fixture_data

    def test_upsert_data_as_anonymous_raises_error(self):
        """test upsert data as anonymous raises error

        Returns:

        """
        mock_user = create_mock_user(user_id=None, is_anonymous=True)
        mock_request = create_mock_request(mock_user)
        with self.assertRaises(AccessControlError):
            data_api.upsert(_create_data("1", None), mock_request)

    def test_upsert_data_with_no_workspace_creates_data(self):
        """test upsert data with no workspace creates data

        Returns:

        """
        mock_user = _create_user(1)
        mock_request = create_mock_request(mock_user)

        data = _create_data(1, None)
        data_api.upsert(data, mock_request)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_upsert_data_in_accessible_creates_data(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test upsert data in accessible creates data

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        mock_request = create_mock_request(mock_user)
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data = _create_data(1, fixture_data.workspace_1)
        data_api.upsert(data, mock_request)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_upsert_data_in_inaccessible_workspace_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test upsert data in inaccessible workspace raises error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        mock_request = create_mock_request(mock_user)
        get_all_workspaces_with_write_access_by_user.return_value = []
        data = _create_data(1, fixture_data.workspace_1)
        with self.assertRaises(AccessControlError):
            data_api.upsert(data, mock_request)

    def test_edit_data_as_anonymous_raises_error(self):
        """test edit data as anonymous raises error

        Returns:

        """
        user = create_mock_user(user_id=None, is_anonymous=True)
        mock_request = create_mock_request(user)
        fixture_data.data_1.title = "new name"
        with self.assertRaises(AccessControlError):
            data_api.upsert(fixture_data.data_1, mock_request)

    def test_edit_others_data_not_in_workspace_raises_error(self):
        """test edit others data not in workspace raises error

        Returns:

        """
        user = create_mock_user(user_id=1)
        mock_request = create_mock_request(user)
        fixture_data.data_2.title = "new name"
        with self.assertRaises(AccessControlError):
            data_api.upsert(fixture_data.data_2, mock_request)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_edit_others_data_in_accessible_workspace_updates_data(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test edit others data in accessible workspace updates data

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        user = create_mock_user(user_id=1)
        mock_request = create_mock_request(user)
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_data.workspace_2
        ]
        fixture_data.data_4.xml_content = (
            '<tag  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ></tag>'
        )
        data_api.upsert(fixture_data.data_4, mock_request)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_edit_others_data_in_inaccessible_workspace_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test edit others data in inaccessible workspace raises error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        user = create_mock_user(user_id=1)
        mock_request = create_mock_request(user)
        get_all_workspaces_with_write_access_by_user.return_value = []
        fixture_data.data_4.title = "new name"
        with self.assertRaises(AccessControlError):
            data_api.upsert(fixture_data.data_4, mock_request)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_edit_own_data_updates_data(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test edit own data updates data

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        user = create_mock_user(user_id=1)
        mock_request = create_mock_request(user)
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        fixture_data.data_3.xml_content = (
            '<tag  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ></tag>'
        )
        data_api.upsert(fixture_data.data_3, mock_request)

    def test_edit_own_data_with_no_workspace_updates_data(self):
        """test edit own data with no workspace updates data

        Returns:

        """
        user = create_mock_user(user_id=1)
        mock_request = create_mock_request(user)
        fixture_data.data_1.xml_content = (
            '<tag  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ></tag>'
        )
        data_api.upsert(fixture_data.data_1, mock_request)


class TestDataExecuteQuery(MongoIntegrationBaseTestCase):
    """TestDataExecuteQuery"""

    fixture = fixture_data

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data_list = data_api.execute_json_query({}, mock_user)
        self.assertTrue(len(data_list) > 0)
        self.assertTrue(all(len(data.title) for data in data_list))

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_returns_data_in_workspace_1(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data in workspace 1

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data_list = data_api.execute_json_query({}, mock_user)
        self.assertTrue(len(data_list) == 2)
        self.assertTrue(str(data.workspace) == "1" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_returns_data_in_workspace_2(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data in workspace 2

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data_list = data_api.execute_json_query({}, mock_user)
        self.assertTrue(len(data_list) == 2)
        self.assertTrue(str(data.workspace) == "2" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_returns_data_in_workspace_1_and_2(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data in workspace 1 and 2

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1,
            fixture_data.workspace_2,
        ]
        data_list = data_api.execute_json_query({}, mock_user)
        self.assertTrue(len(data_list) == 3)
        self.assertTrue(
            str(data.workspace) == "1" or str(data.workspace) == "2"
            for data in data_list
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_force_workspace_1_returns_data_from_workspace_1(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query force workspace 1 returns data from workspace 1

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data_list = data_api.execute_json_query(
            {"workspace": fixture_data.workspace_1.id}, mock_user
        )
        self.assertTrue(len(data_list) == 2)
        self.assertTrue(str(data.workspace) == "1" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_force_workspace_1_raises_acl_error_if_no_access(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query force workspace 1 raises acl error if no access

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(
                {"workspace": fixture_data.workspace_1.id}, mock_user
            )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_execute_query_force_workspace_none_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query force workspace none raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query({"workspace": None}, mock_user)

    def test_execute_query_as_superuser_returns_all_data(self):
        """test execute query as superuser returns all data

        Returns:

        """
        mock_user = _create_user(1, is_superuser=True)
        data_list = data_api.execute_json_query({}, mock_user)
        self.assertTrue(len(data_list) == 5)


class TestDataExecuteRawQuery(MongoIntegrationBaseTestCase):
    """TestDataExecuteRawQuery"""

    fixture = fixture_data2

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_all_data_returns_private_data_of_user_1(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns private data of user 1

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(str(data.user_id) == "1" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_all_data_returns_private_data_of_user_2(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns private data of user 2

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(2)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(str(data.user_id) == "2" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_all_data_returns_private_data_of_user_3(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns private data of user 3

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(str(data.user_id) == "3" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_all_data_returns_accessible_data_of_user_1(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns accessible data of user 1

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(
            str(data.user_id) == "1" or str(data.workspace) == "1" for data in data_list
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_all_data_returns_accessible_data_of_user_2(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns accessible data of user 2

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(2)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(
            str(data.user_id) == "2" or str(data.workspace) == "1" for data in data_list
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_all_data_returns_accessible_data_of_user_3(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns accessible data of user 3

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(
            str(data.user_id) == "3" or str(data.workspace) == "1" for data in data_list
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_private_data_from_other_user_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test get private data from other user raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"user_id": 1}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_data_from_workspace_without_access_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test get data from workspace without access raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(4)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"workspace": 1}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_on_workspace_without_access_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query on workspace without access raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(4)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$or": [{"workspace": 1}]}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_in_workspace_without_access_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query in workspace without access raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(4)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"workspace": {"$in": [1, 2]}}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_workspace_none_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query workspace none raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"workspace": None}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_workspace_none_with_read_access_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query workspace none with read access raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        query = {"workspace": None}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_workspace_in_none_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query workspace in none raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        query = {"workspace": {"$in": [None, 1]}}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_workspace_none_and_one_with_read_access_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query workspace none raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        query = {"workspace": {"$in": [None, 1]}}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_others_data_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query others data raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        query = {"user_id": 3}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_others_data_in_no_workspace_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query others data in no workspace raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"user_id": 3, "workspace": None}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_others_data_in_workspace_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query others data in workspace raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        query = {"user_id": 3, "workspace": 1}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_others_data_in_workspace_as_superuser_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query others data in workspace as superuser returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1, is_superuser=True)
        get_all_workspaces_with_read_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        query = {"user_id": 3, "workspace": self.fixture.workspace_1.id}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(
            str(data.user_id) == "3" and str(data.workspace) == "1"
            for data in data_list
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_in_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query in with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$in": ["value2", "value3"]}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(data.user_id == "3" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_in_without_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query in without matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$in": ["value3"]}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_regex_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query regex with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$regex": ".*"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(data.user_id == "3" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_regex_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query regex without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$regex": "aaa"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_pattern_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query pattern with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": re.compile(".*")}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(data.user_id == "3" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_pattern_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query pattern without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": re.compile("aaa")}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_not_pattern_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query not pattern with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$not": re.compile("aaa")}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(data.user_id == "3" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_not_pattern_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query not pattern without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$not": re.compile(".*")}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_exists_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query exists with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$exists": True}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() != 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_exists_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query exists without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.absent": {"$exists": True}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_ne_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query ne without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$ne": "value2"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_ne_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query ne with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$ne": "aaa"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_ne_with_inaccessible_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query ne with inaccessible matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(4)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$ne": "aaa"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_not_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query not without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$not": {"$regex": "value2"}}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_not_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query not with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$not": {"$regex": "aaa"}}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_not_with_inaccessible_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query not with inaccessible matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(4)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$not": {"$regex": "aaa"}}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)


class TestDataExecuteFullTextQuery(MongoIntegrationBaseTestCase):
    """TestDataExecuteFullTextQuery"""

    fixture = fixture_data_full_text

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_full_text_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$text": {"$search": "user1"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)
        self.assertEqual(data_list[0], self.fixture.data_1)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_full_text_with_multiple_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with multiple matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        query = {"$text": {"$search": "value1"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 2)
        self.assertIn(self.fixture.data_1, data_list)
        self.assertIn(self.fixture.data_2, data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_full_text_with_multiple_words_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with multiple words returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$text": {"$search": "value1 user1"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)
        self.assertIn(self.fixture.data_1, data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_full_text_with_multiple_words_but_one_incorrect_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with multiple words but one incorrect returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        query = {"$text": {"$search": "value1 user2"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_full_text_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$text": {"$search": "wrong"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_full_text_with_private_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with private matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user("2")
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$text": {"$search": "user1"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_query_full_text_with_inaccessible_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with inaccessible matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user("3")
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$text": {"$search": "value1"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)


class TestDataDelete(MongoIntegrationBaseTestCase):
    """TestDataDelete"""

    fixture = fixture_data

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_data_in_accessible_workspace_deletes_data(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test delete own data in accessible workspace deletes data

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        data_api.delete(
            fixture_data.data_collection[fixture_data.USER_1_WORKSPACE_1], mock_user
        )

    # FIXME: test is not true.
    #  Deleting own data in workspace without write access raises ACL error
    #  (FIXME note also found in ACL code.)
    @unittest.skip("Test is not True.")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_data_in_not_accessible_workspace_deletes_data(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test delete own data in not accessible workspace deletes data

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []
        data_api.delete(
            fixture_data.data_collection[fixture_data.USER_1_WORKSPACE_1], mock_user
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_others_data_in_accessible_workspace_deletes_data(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test delete others data in accessible workspace deletes data

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
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
        """test delete others data not accessible workspace raises error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_data.workspace_1
        ]
        with self.assertRaises(AccessControlError):
            data_api.delete(
                fixture_data.data_collection[fixture_data.USER_2_WORKSPACE_2], mock_user
            )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_data_not_in_workspace_deletes_data(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test delete own data not in workspace deletes data

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
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
        """test delete others data not in workspace raises error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.delete(
                fixture_data.data_collection[fixture_data.USER_2_NO_WORKSPACE],
                mock_user,
            )


class TestDataChangeOwner(MongoIntegrationBaseTestCase):
    """TestDataChangeOwner"""

    fixture = fixture_data

    def test_change_owner_from_owner_to_owner_ok(self):
        """test change owner from owner to owner ok

        Returns:

        """
        mock_owner = _create_user(1)
        data_api.change_owner(
            document=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
            new_user=mock_owner,
            user=mock_owner,
        )

    def test_change_owner_from_owner_to_user_ok(self):
        """test change owner from owner to user ok

        Returns:

        """
        mock_owner = _create_user(1)
        mock_user = _create_user(2)
        data_api.change_owner(
            document=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
            new_user=mock_user,
            user=mock_owner,
        )

    def test_change_owner_from_user_to_user_raises_exception(self):
        """test change owner from user to user raises exception

        Returns:

        """
        mock_owner = _create_user(1)
        mock_user = _create_user(2)
        with self.assertRaises(AccessControlError):
            data_api.change_owner(
                document=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
                new_user=mock_owner,
                user=mock_user,
            )

    def test_change_owner_as_superuser_ok(self):
        """test change owner as superuser ok

        Returns:

        """
        mock_user = _create_user(2, is_superuser=True)
        data_api.change_owner(
            document=fixture_data.data_collection[fixture_data.USER_1_NO_WORKSPACE],
            new_user=mock_user,
            user=mock_user,
        )


def _create_user(user_id, is_superuser=False):
    """create user

    Args:
        user_id:
        is_superuser:

    Returns:

    """
    return create_mock_user(user_id, is_superuser=is_superuser)


def _create_data(user_id, workspace):
    """create data

    Args:
        user_id:
        workspace:

    Returns:

    """
    return Data(
        template=fixture_data.template,
        title="DataTitle",
        user_id=str(user_id),
        xml_content='<tag  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ></tag>',
        workspace=workspace,
    )
