""" Access control testing
"""
import re
import unittest
from unittest.mock import patch

from django.test import override_settings, tag

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import QueryError
from core_main_app.components.data import api as data_api
from core_main_app.components.mongo import api as mongo_data_api
from core_main_app.permissions.discover import init_mongo_indexing
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoDBIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestDataExecuteQuery(MongoDBIntegrationBaseTestCase):
    """TestDataExecuteQuery"""

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    def setUp(self):
        """Insert needed data.

        Returns:

        """
        from core_main_app.components.mongo.models import (  # noqa: keep import to init signals
            MongoData,
        )
        from tests.components.data.fixtures.fixtures import (
            AccessControlDataFixture,
        )

        # Mongo indexing is not initialized by default
        init_mongo_indexing()

        # fixture needs to initialized with settings.MONGODB_INDEXING=True otherwise MongoData does not exist
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        data_list = data_api.execute_json_query({}, mock_user)
        self.assertTrue(len(data_list) > 0)
        self.assertTrue(all(len(data.title) for data in data_list))

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_returns_data_in_workspace_1(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data in workspace 1

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        data_list = data_api.execute_json_query({}, mock_user)
        self.assertTrue(len(data_list) == 2)
        self.assertTrue(str(data.workspace) == "1" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_returns_data_in_workspace_2(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data in workspace 2

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        data_list = data_api.execute_json_query({}, mock_user)
        self.assertTrue(len(data_list) == 2)
        self.assertTrue(str(data.workspace) == "2" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_returns_data_in_workspace_1_and_2(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data in workspace 1 and 2

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1,
            self.fixture.workspace_2,
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
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_force_workspace_1_returns_data_from_workspace_1(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query force workspace 1 returns data from workspace 1

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        data_list = data_api.execute_json_query(
            {"workspace": self.fixture.workspace_1.id}, mock_user
        )
        self.assertTrue(len(data_list) == 2)
        self.assertTrue(str(data.workspace) == "1" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_force_workspace_1_raises_acl_error_if_no_access(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query force workspace 1 raises acl error if no access

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(
                {"workspace": self.fixture.workspace_1.id}, mock_user
            )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_force_workspace_none_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query force workspace none raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query({"workspace": None}, mock_user)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_as_superuser_returns_all_data(self):
        """test execute query as superuser returns all data

        Returns:

        """
        mock_user = create_mock_user(1, is_superuser=True)
        data_list = data_api.execute_json_query({}, mock_user)
        self.assertTrue(len(data_list) == 5)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_as_superuser_with_unknown_operator_raises_error(
        self,
    ):
        """test_execute_query_as_superuser_with_unknown_operator_raises_error

        Returns:

        """
        mock_user = create_mock_user(1, is_superuser=True)
        with self.assertRaises(QueryError):
            data_api.execute_json_query({"$test": True}, mock_user)

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=False)
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_as_anonymous_raises_error_if_no_anonymous_access(
        self,
    ):
        """test_execute_query_as_anonymous_returns_no_data_if_no_anonymous_access

        Returns:

        """
        mock_user = create_mock_user(None, is_anonymous=True)
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query({}, mock_user)

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_as_anonymous_returns_only_public_data_if_anonymous_access(
        self,
    ):
        """test_execute_query_as_anonymous_returns_public_data_if_anonymous_access

        Returns:

        """
        mock_user = create_mock_user(None, is_anonymous=True)
        data_list = data_api.execute_json_query({}, mock_user)
        # no public data in the fixture
        self.assertEqual(data_list.count(), 0)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_with_template_returns_data(
        self,
    ):
        """test_execute_query_with_template_returns_data

        Returns:

        """
        mock_user = create_mock_user(None, is_superuser=True)
        data_list = data_api.execute_json_query(
            {"template": self.fixture.template.id}, mock_user
        )
        # no public data in the fixture
        self.assertEqual(data_list.count(), 5)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_with_unknown_template_id_returns_no_data(
        self,
    ):
        """test_execute_query_with_unknown_template_id_returns_no_data

        Returns:

        """
        mock_user = create_mock_user(None, is_superuser=True)
        data_list = data_api.execute_json_query({"template": -1}, mock_user)
        # no public data in the fixture
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_get_owned_data_returns_only_owned_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        data_list = data_api.execute_json_query({"user_id": "3"}, mock_user)
        self.assertEqual(len(data_list), 0)
        self.assertTrue(all(data.user_id == "3" for data in data_list))

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_get_by_empty_workspace_list(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        data_list = data_api.execute_json_query({"workspace": []}, mock_user)
        self.assertEqual(len(data_list), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_and_workspace_user_as_superuser(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3, is_superuser=True)
        get_all_workspaces_with_read_access_by_user.return_value = []
        data_list = data_api.execute_json_query(
            {"$and": [{"workspace": 1}, {"user_id": 3}]}, mock_user
        )
        self.assertEqual(len(data_list), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_and_workspace_user_as_user_raises_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(
                {"$and": [{"workspace": 1}, {"user_id": 3}]}, mock_user
            )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_with_workspace_id_returns_no_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test execute query returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        data_list = data_api.execute_json_query(
            {"_workspace_id": 1}, mock_user
        )
        self.assertEqual(data_list.count(), 0)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_as_superuser_with_unknown_operator_value_raises_error(
        self,
    ):
        """test_execute_query_as_superuser_with_unknown_operator_value_raises_error

        Returns:

        """
        mock_user = create_mock_user(1, is_superuser=True)
        with self.assertRaises(QueryError):
            data_api.execute_json_query({"test": "$2"}, mock_user)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_as_superuser_with_unknown_operator_in_list_raises_error(
        self,
    ):
        """test_execute_query_as_superuser_with_unknown_operator_in_list_raises_error

        Returns:

        """
        mock_user = create_mock_user(1, is_superuser=True)
        with self.assertRaises(QueryError):
            data_api.execute_json_query(
                {"$and": [{"$or": [{"root.element": {"$test": ["1", "2"]}}]}]},
                mock_user,
            )

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_as_superuser_with_unknown_operator_in_value_raises_error(
        self,
    ):
        """test_execute_query_as_superuser_with_unknown_operator_in_value_raises_error

        Returns:

        """
        mock_user = create_mock_user(1, is_superuser=True)
        with self.assertRaises(QueryError):
            data_api.execute_json_query(
                {
                    "$and": [
                        {"$or": [{"root.element": {"$in": ["$test", "2"]}}]}
                    ]
                },
                mock_user,
            )

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_as_superuser_with_unknown_operator_in_key_raises_error(
        self,
    ):
        """test_execute_query_as_superuser_with_unknown_operator_in_key_raises_error

        Returns:

        """
        mock_user = create_mock_user(1, is_superuser=True)
        with self.assertRaises(QueryError):
            data_api.execute_json_query(
                {"$and": [{"$or": [{"root.$element": {"$in": ["1", "2"]}}]}]},
                mock_user,
            )

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_execute_query_as_superuser_with_where_operator_in_key_raises_error(
        self,
    ):
        """test_execute_query_as_superuser_with_where_operator_in_key_raises_error

        Returns:

        """
        mock_user = create_mock_user(1, is_superuser=True)
        with self.assertRaises(QueryError):
            data_api.execute_json_query(
                {
                    "$and": [
                        {"$or": [{"root.element": {"$where": ["1", "2"]}}]}
                    ]
                },
                mock_user,
            )


class TestDataExecuteRawQuery(MongoDBIntegrationBaseTestCase):
    """TestDataExecuteRawQuery"""

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def setUp(self):
        """Insert needed data.

        Returns:

        """
        from core_main_app.components.mongo.models import (  # noqa: keep import to init signals
            MongoData,
        )
        from tests.components.data.fixtures.fixtures import (
            AccessControlDataFixture2,
        )

        # Mongo indexing is not initialized by default
        init_mongo_indexing()

        # fixture needs to initialized with settings.MONGODB_INDEXING=True otherwise
        # MongoData does not exist
        self.fixture = AccessControlDataFixture2()
        self.fixture.insert_data()

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_all_data_returns_private_data_of_user_1(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns private data of user 1

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(str(data.user_id) == "1" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_all_data_returns_private_data_of_user_2(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns private data of user 2

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(2)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(str(data.user_id) == "2" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_all_data_returns_private_data_of_user_3(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns private data of user 3

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(str(data.user_id) == "3" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_all_data_returns_accessible_data_of_user_1(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns accessible data of user 1

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(
            str(data.user_id) == "1" or str(data.workspace) == "1"
            for data in data_list
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_all_data_returns_accessible_data_of_user_2(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns accessible data of user 2

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(2)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(
            str(data.user_id) == "2" or str(data.workspace) == "1"
            for data in data_list
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_all_data_returns_accessible_data_of_user_3(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query all data returns accessible data of user 3

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        query = {}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(
            str(data.user_id) == "3" or str(data.workspace) == "1"
            for data in data_list
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_get_private_data_from_other_user_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test get private data from other user raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"user_id": 1}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_get_data_from_workspace_without_access_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test get data from workspace without access raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(4)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"workspace": 1}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_on_workspace_without_access_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query on workspace without access raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(4)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$or": [{"workspace": 1}]}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_in_workspace_without_access_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query in workspace without access raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(4)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"workspace": {"$in": [1, 2]}}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_workspace_none_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query workspace none raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"workspace": None}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_workspace_none_as_superuser_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_query_workspace_none_as_superuser_returns_data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1, is_superuser=True)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"workspace": None}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() == 2)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_workspace_none_with_read_access_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query workspace none with read access raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        query = {"workspace": None}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_workspace_in_none_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query workspace in none raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        query = {"workspace": {"$in": [None, 1]}}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_workspace_none_and_one_with_read_access_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query workspace none raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        query = {"workspace": {"$in": [None, 1]}}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_others_data_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query others data raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        query = {"user_id": 3}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_others_data_in_no_workspace_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query others data in no workspace raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"user_id": 3, "workspace": None}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_others_data_in_workspace_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query others data in workspace raises acl error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        query = {"user_id": 3, "workspace": 1}
        with self.assertRaises(AccessControlError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_others_data_in_workspace_as_superuser_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query others data in workspace as superuser returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1, is_superuser=True)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
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
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_in_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query in with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$in": ["value2", "value3"]}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(data.user_id == "3" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_in_without_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query in without matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$in": ["value3"]}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_regex_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query regex with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$regex": ".*"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(data.user_id == "3" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_regex_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query regex without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$regex": "aaa"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_pattern_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query pattern with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": re.compile(".*")}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(data.user_id == "3" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_pattern_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query pattern without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": re.compile("aaa")}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_not_pattern_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query not pattern with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$not": re.compile("aaa")}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() > 0)
        self.assertTrue(data.user_id == "3" for data in data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_not_pattern_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query not pattern without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$not": re.compile(".*")}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_exists_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query exists with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$exists": True}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() != 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_exists_false_raises_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_query_exists_false_raises_error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$exists": False}}
        with self.assertRaises(QueryError):
            data_api.execute_json_query(query, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_exists_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query exists without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(3)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.absent": {"$exists": True}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertTrue(data_list.count() == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_ne_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query ne without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$ne": "value2"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_ne_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query ne with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$ne": "aaa"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_ne_with_inaccessible_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query ne with inaccessible matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(4)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$ne": "aaa"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_not_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query not without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$not": {"$regex": "value2"}}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_not_regex_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query not with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$not": {"$regex": "aaa"}}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_not_regex_with_inaccessible_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query not with inaccessible matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(4)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$not": {"$regex": "aaa"}}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_exact_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_query_exact_with_matches_returns_data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": "value2"}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_exact_with_no_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_query_exact_with_no_matches_returns_nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": "value3"}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_eq_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_query_eq_with_matches_returns_data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$eq": "value2"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_eq_with_no_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_query_eq_with_no_matches_returns_nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": {"$eq": "value3"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)


class TestDataExecuteNoneQuery(MongoDBIntegrationBaseTestCase):
    """TestDataExecuteNoneQuery"""

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    def setUp(self):
        """Insert needed data.

        Returns:

        """
        from core_main_app.components.mongo.models import (  # noqa: keep import to init signals
            MongoData,
        )
        from tests.components.data.fixtures.fixtures import (
            AccessControlDataNoneFixture,
        )

        # Mongo indexing is not initialized by default
        init_mongo_indexing()

        # fixture needs to initialized with settings.MONGODB_INDEXING=True otherwise MongoData does not exist
        self.fixture = AccessControlDataNoneFixture()
        self.fixture.insert_data()

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_none_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_query_none_with_matches_returns_data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": None}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_query_none_with_no_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_query_none_with_no_matches_returns_nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user(2)
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"dict_content.root.element": None}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)


class TestDataExecuteFullTextQuery(MongoDBIntegrationBaseTestCase):
    """TestDataExecuteFullTextQuery"""

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    def setUp(self):
        """Insert needed data.

        Returns:

        """
        from core_main_app.components.mongo.models import (  # noqa: keep import to init signals
            MongoData,
        )
        from tests.components.data.fixtures.fixtures import (
            AccessControlDataFullTextSearchFixture,
        )

        # Mongo indexing is not initialized by default
        init_mongo_indexing()

        # fixture needs to initialized with settings.MONGODB_INDEXING=True otherwise MongoData does not exist
        self.fixture = AccessControlDataFullTextSearchFixture()
        self.fixture.insert_data()

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    @unittest.skip("The $text operator is not implemented in mongomock yet")
    def test_query_full_text_with_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$text": {"$search": "user1"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)
        self.assertEqual(data_list[0], self.fixture.data_1)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    @unittest.skip("The $text operator is not implemented in mongomock yet")
    def test_query_full_text_with_multiple_matches_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with multiple matches returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user("1")
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
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    @unittest.skip("The $text operator is not implemented in mongomock yet")
    def test_query_full_text_with_multiple_words_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with multiple words returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$text": {"$search": "value1 user1"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)
        self.assertIn(self.fixture.data_1, data_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    @unittest.skip("The $text operator is not implemented in mongomock yet")
    def test_query_full_text_with_multiple_words_but_one_incorrect_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with multiple words but one incorrect returns data

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        query = {"$text": {"$search": "value1 user2"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    @unittest.skip("The $text operator is not implemented in mongomock yet")
    def test_query_full_text_without_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text without matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$text": {"$search": "wrong"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    @unittest.skip("The $text operator is not implemented in mongomock yet")
    def test_query_full_text_with_private_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with private matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user("2")
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$text": {"$search": "user1"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    @unittest.skip("The $text operator is not implemented in mongomock yet")
    def test_query_full_text_with_inaccessible_matches_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test query full text with inaccessible matches returns nothing

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user("3")
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$text": {"$search": "value1"}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    @unittest.skip("The $text operator is not implemented in mongomock yet")
    def test_query_full_text_with_invalid_value_raises_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_query_full_text_with_invalid_value_raises_error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = create_mock_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        query = {"$text": {"$search": 1}}
        with self.assertRaises(QueryError):
            data_api.execute_json_query(query, mock_user)


class TestDataExecuteNumericQuery(MongoDBIntegrationBaseTestCase):
    """TestDataExecuteFullTextQuery"""

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    def setUp(self):
        """Insert needed data.

        Returns:

        """
        from core_main_app.components.mongo.models import (  # noqa: keep import to init signals
            MongoData,
        )
        from tests.components.data.fixtures.fixtures import (
            AccessControlDataNumericFixture,
        )

        # Mongo indexing is not initialized by default
        init_mongo_indexing()

        # fixture needs to initialized with settings.MONGODB_INDEXING=True otherwise MongoData does not exist
        self.fixture = AccessControlDataNumericFixture()
        self.fixture.insert_data()

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_exact_matches_returns_data(
        self,
    ):
        """test_exact_matches_returns_data

        Args:
            :

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        query = {"dict_content.root.element": 1}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_exact_without_matches_returns_nothing(
        self,
    ):
        """test_exact_without_matches_returns_nothing

        Args:
            :

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        query = {"dict_content.root.element": 8}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_eq_matches_returns_data(
        self,
    ):
        """test_eq_matches_returns_data

        Args:
            :

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        query = {"dict_content.root.element": {"$eq": 1}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_eq_without_matches_returns_nothing(
        self,
    ):
        """test_eq_without_matches_returns_nothing

        Args:
            :

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        query = {"dict_content.root.element": {"$eq": 8}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 0)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_lte_matches_returns_data(
        self,
    ):
        """test_lte_matches_returns_data

        Args:
            :

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        query = {"dict_content.root.element": {"$lte": 2}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 2)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_lt_matches_returns_data(
        self,
    ):
        """test_lt_matches_returns_data

        Args:
            :

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        query = {"dict_content.root.element": {"$lt": 2}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 1)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_gt_matches_returns_data(
        self,
    ):
        """test_gt_matches_returns_data

        Args:
            :

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        query = {"dict_content.root.element": {"$gt": 2}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 2)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_gte_matches_returns_data(
        self,
    ):
        """test_gte_matches_returns_data

        Args:
            :

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        query = {"dict_content.root.element": {"$gte": 2}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 3)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_ne_matches_returns_data(
        self,
    ):
        """test_ne_matches_returns_data

        Args:
            :

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        query = {"dict_content.root.element": {"$ne": 2}}
        data_list = data_api.execute_json_query(query, mock_user)
        self.assertEqual(data_list.count(), 3)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_numeric_operators_raises_error_if_not_numeric_value(self):
        """test_numeric_operators_raises_error_if_not_numeric_value

        Args:

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        for operator in ["$lt", "$lte", "$gt", "$gte"]:
            for value in ["test", "$1", None]:
                with self.assertRaises(QueryError):
                    data_api.execute_json_query(
                        {"dict_content.root.element": {operator: value}},
                        mock_user,
                    )

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_numeric_operators_raises_no_error_if_numeric_value(self):
        """test_numeric_operators_raises_no_error_if_numeric_value

        Args:

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        for operator in ["$lt", "$lte", "$gt", "$gte"]:
            for value in [0, 1, 1.2]:
                data_api.execute_json_query(
                    {"dict_content.root.element": {operator: value}}, mock_user
                )


class TestAggregateData(MongoDBIntegrationBaseTestCase):
    """TestDataExecuteFullTextQuery"""

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    def setUp(self):
        """Insert needed data.

        Returns:

        """
        from core_main_app.components.mongo.models import (  # noqa: keep import to init signals
            MongoData,
        )
        from tests.components.data.fixtures.fixtures import (
            AccessControlDataFixture,
        )

        # Mongo indexing is not initialized by default
        init_mongo_indexing()

        # fixture needs to initialized with settings.MONGODB_INDEXING=True otherwise MongoData does not exist
        self.fixture = AccessControlDataFixture()
        self.fixture.insert_data()

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_aggregate_as_superuser_returns_data(
        self,
    ):
        """test_aggregate_as_superuser_returns_data

        Args:
            :

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        self.assertIsNotNone(mongo_data_api.aggregate({}, user=mock_user))

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_aggregate_as_anonymous_raises_error(
        self,
    ):
        """test_aggregate_as_anonymous_raises_error

        Args:
            :

        Returns:

        """
        mock_user = create_mock_user(None, is_anonymous=True)
        with self.assertRaises(AccessControlError):
            mongo_data_api.aggregate({}, user=mock_user)


class TestDataBlob(MongoDBIntegrationBaseTestCase):
    """TestDataBlob"""

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    def setUp(self):
        """Insert needed data.

        Returns:

        """
        from core_main_app.components.mongo.models import (  # noqa: keep import to init signals
            MongoData,
        )
        from tests.components.data.fixtures.fixtures import (
            AccessControlBlobWithMetadataFixture,
        )

        # Mongo indexing is not initialized by default
        init_mongo_indexing()

        # fixture needs to initialized with settings.MONGODB_INDEXING=True otherwise MongoData does not exist
        self.fixture = AccessControlBlobWithMetadataFixture()
        self.fixture.insert_data()

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_data_blob_as_owner_returns_blob(
        self,
    ):
        """test_data_blob_as_owner_returns_blob

        Args:
            :

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        mock_user = create_mock_user("1")
        mongo_data_1 = MongoData.objects.get(data_id=self.fixture.data_1.id)
        blob = mongo_data_1.blob(mock_user)
        self.assertEqual(blob, self.fixture.blob_1)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_data_blob_as_anonymous_raises_acl_error(self):
        """test_data_blob_as_anonymous_raises_acl_error

        Args:

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        mock_user = create_mock_user("2", is_anonymous=True)
        mongo_data_1 = MongoData.objects.get(data_id=self.fixture.data_1.id)
        with self.assertRaises(AccessControlError):
            mongo_data_1.blob(mock_user)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    def test_data_blob_as_superuser_returns_blob(
        self,
    ):
        """test_data_blob_as_superuser_returns_blob

        Args:

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        mock_user = create_mock_user("2", is_superuser=True)
        mongo_data_1 = MongoData.objects.get(data_id=self.fixture.data_1.id)
        blob = mongo_data_1.blob(mock_user)
        self.assertEqual(blob, self.fixture.blob_1)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_data_private_blob_as_other_user_raises_acl_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_data_private_blob_as_other_user_raises_acl_error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        data = MongoData.objects.get(data_id=self.fixture.data_1.id)
        mock_user = create_mock_user(2)
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data.blob(mock_user)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_data_other_user_blob_in_workspace_with_access_returns_blob(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_data_other_user_blob_in_workspace_with_access_returns_blob

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        data = MongoData.objects.get(data_id=self.fixture.data_2.id)
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        blob = data.blob(mock_user)
        self.assertEqual(blob, self.fixture.blob_2)

    @override_settings(MONGODB_INDEXING=True)
    @override_settings(MONGODB_ASYNC_SAVE=False)
    @tag("mongodb")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_data_other_user_blob_in_workspace_without_access_raises_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_data_other_user_blob_in_workspace_without_access_raises_error

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        data = MongoData.objects.get(data_id=self.fixture.data_2.id)
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            data.blob(mock_user)
