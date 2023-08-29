""" Unit tests for `core_main_app.components.data.access_control`.
"""
from unittest import TestCase
from unittest.mock import patch

from unittest.mock import MagicMock

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.components.data import access_control as data_acl


class TestCanReadAggregateQuery(TestCase):
    """Unit tests for `can_read_aggregate_query` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_kwargs = {
            "func": MagicMock(),
            "query": MagicMock(),
            "user": create_mock_user("1"),
        }

    @patch.object(data_acl, "_update_can_read_aggregate_query")
    @patch.object(data_acl, "check_anonymous_access")
    def test_superuser_returns_func_with_args(
        self, mock_check_anonymous_access, mock_update_can_read_aggregate_query
    ):
        """test_superuser_returns_func_with_args"""
        self.mock_kwargs["user"] = create_mock_user("1", is_superuser=True)

        self.assertEqual(
            data_acl.can_read_aggregate_query(**self.mock_kwargs),
            self.mock_kwargs["func"](
                self.mock_kwargs["query"], self.mock_kwargs["user"]
            ),
        )

    @patch.object(data_acl, "_update_can_read_aggregate_query")
    @patch.object(data_acl, "check_anonymous_access")
    def test_check_anonymous_access_called(
        self, mock_check_anonymous_access, mock_update_can_read_aggregate_query
    ):
        """test_check_anonymous_access_called"""

        data_acl.can_read_aggregate_query(**self.mock_kwargs)
        mock_check_anonymous_access.assert_called_with(
            self.mock_kwargs["user"]
        )

    @patch.object(data_acl, "_update_can_read_aggregate_query")
    @patch.object(data_acl, "check_anonymous_access")
    def test_update_can_read_aggregate_query_called(
        self, mock_check_anonymous_access, mock_update_can_read_aggregate_query
    ):
        """test_update_can_read_aggregate_query_called"""

        data_acl.can_read_aggregate_query(**self.mock_kwargs)
        mock_update_can_read_aggregate_query.assert_called_with(
            self.mock_kwargs["query"], self.mock_kwargs["user"]
        )

    @patch.object(data_acl, "_update_can_read_aggregate_query")
    @patch.object(data_acl, "check_anonymous_access")
    def test_returns_func_with_args(
        self, mock_check_anonymous_access, mock_update_can_read_aggregate_query
    ):
        """test_returns_func_with_args"""

        self.assertEqual(
            data_acl.can_read_aggregate_query(**self.mock_kwargs),
            self.mock_kwargs["func"](
                self.mock_kwargs["query"], self.mock_kwargs["user"]
            ),
        )
