""" Unit test for rest views
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.test import override_settings, tag
from importlib.metadata import PackageNotFoundError

from core_main_app.rest.views import CoreSettings
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestCoreSetting(TestCase):
    """TestCoreSetting"""

    def test_anonymous_user_access_denied(self):
        """test_anonymous_user_access_denied

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            CoreSettings.as_view(),
            None,
        )

        # Assert
        self.assertEqual(response.status_code, 403)

    def test_user_get_response(self):
        """test_user_get_response

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            CoreSettings.as_view(),
            mock_user,
        )

        # Assert
        self.assertEqual(response.status_code, 200)

    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.utils.databases.mongo.MONGO_CLIENT", MagicMock())
    @tag("mongodb")
    def test_user_get_mongodb_info(self):
        """test_user_get_mongodb_info

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            CoreSettings.as_view(),
            mock_user,
        )

        # Assert
        self.assertEqual(response.data["mongodb"]["data_indexing"], True)

    def test_user_get_psql_info(self):
        """test_user_get_psql_info

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            CoreSettings.as_view(),
            mock_user,
        )

        # Assert
        self.assertEqual(response.data["database"]["engine"], "PostgreSQL")

    @tag("sqlite3")
    def test_user_get_sqlite_info(self):
        """test_user_get_sqlite_info

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            CoreSettings.as_view(),
            mock_user,
        )

        # Assert
        self.assertEqual(response.data["database"]["engine"], "SQLite3")

    @patch("core_main_app.utils.databases.backend.get_default_database_engine")
    def test_user_get_info_of_other_engine_returns_none(
        self,
        get_default_database_engine,
    ):
        """test_user_get_info_of_other_engine_returns_none

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        get_default_database_engine.return_value = "Other"

        # Act
        response = RequestMock.do_request_get(
            CoreSettings.as_view(),
            mock_user,
        )

        # Assert
        self.assertEqual(response.data["database"]["engine"], None)

    @patch("importlib.metadata.version")
    def test_main_app_not_found_returns_none(self, version):
        """test_main_app_not_found_returns_none

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        version.side_effect = PackageNotFoundError()

        # Act
        response = RequestMock.do_request_get(
            CoreSettings.as_view(),
            mock_user,
        )

        # Assert
        self.assertEqual(response.data["core_version"], None)
