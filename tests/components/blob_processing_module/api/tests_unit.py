""" Unit tests for `core_main_app.components.blob_processing_module.api` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.blob_processing_module import (
    api as blob_processing_module_api,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestGetAll(TestCase):
    """Unit test for `get_all` function."""

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(blob_processing_module_api, "BlobProcessingModule")
    def test_returns_model_get_all(
        self, mock_blob_processing_module, mock_user_is_registered  # noqa
    ):
        """test_returns_model_get_all"""
        blob_processing_module_api.get_all(MagicMock())

        mock_blob_processing_module.get_all.assert_called_with()


class TestGetById(TestCase):
    """Unit test for `get_by_id` function."""

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(blob_processing_module_api, "BlobProcessingModule")
    def test_returns_model_get_by_id(
        self, mock_blob_processing_module, mock_user_is_registered  # noqa
    ):
        """test_returns_model_get_by_id"""
        mock_blob_module_id = MagicMock()
        blob_processing_module_api.get_by_id(mock_blob_module_id, MagicMock())

        mock_blob_processing_module.get_by_id.assert_called_with(
            mock_blob_module_id
        )


class TestGetAllByBlobId(TestCase):
    """Unit test for `get_all_by_blob_id` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "blob_id": MagicMock(),
            "user": MagicMock(),
            "run_strategy": MagicMock(),
        }

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(blob_processing_module_api, "blob_api")
    @patch.object(blob_processing_module_api, "get_all")
    def test_blob_get_by_id_called(
        self, mock_get_all, mock_blob_api, mock_user_is_registered  # noqa
    ):
        """test_blob_get_by_id_called"""
        mock_get_all.return_value = MagicMock()

        blob_processing_module_api.get_all_by_blob_id(**self.mock_kwargs)

        mock_blob_api.get_by_id.assert_called_with(
            self.mock_kwargs["blob_id"], self.mock_kwargs["user"]
        )

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(blob_processing_module_api, "blob_api")
    @patch.object(blob_processing_module_api, "get_all")
    def test_blob_module_get_all_called(
        self, mock_get_all, mock_blob_api, mock_user_is_registered  # noqa
    ):
        """test_blob_module_get_all_called"""
        mock_get_all.return_value = MagicMock()

        blob_processing_module_api.get_all_by_blob_id(**self.mock_kwargs)

        mock_get_all.assert_called_with(self.mock_kwargs["user"])

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(blob_processing_module_api, "blob_api")
    @patch.object(blob_processing_module_api, "get_all")
    def test_run_strategy_null_does_not_filter(
        self, mock_get_all, mock_blob_api, mock_user_is_registered  # noqa
    ):
        """test_run_strategy_null_does_not_filter"""
        self.mock_kwargs["run_strategy"] = None  # noqa
        mock_blob_module_list = MagicMock()
        mock_get_all.return_value = mock_blob_module_list

        blob_processing_module_api.get_all_by_blob_id(**self.mock_kwargs)

        mock_blob_module_list.filter.assert_not_called()

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(blob_processing_module_api, "blob_api")
    @patch.object(blob_processing_module_api, "get_all")
    def test_run_strategy_not_null_does_filter(
        self, mock_get_all, mock_blob_api, mock_user_is_registered  # noqa
    ):
        """test_run_strategy_not_null_does_filter"""
        mock_blob_module_list = MagicMock()
        mock_get_all.return_value = mock_blob_module_list

        blob_processing_module_api.get_all_by_blob_id(**self.mock_kwargs)

        mock_blob_module_list.filter.assert_called_with(
            run_strategy_list__contains=self.mock_kwargs["run_strategy"]
        )


class TestDelete(TestCase):
    """Unit tests for `delete` function."""

    def setUp(self):
        """setUp"""
        self.non_staff_user = create_mock_user(1, is_staff=False)
        self.staff_user = create_mock_user(1, is_staff=True)
        self.mock_kwargs = {"blob_module_id": 1, "user": self.staff_user}

    def test_non_staff_raise_access_control_error(self):
        """test_non_staff_raise_access_control_error"""
        self.mock_kwargs["user"] = self.non_staff_user

        with self.assertRaises(AccessControlError):
            blob_processing_module_api.delete(**self.mock_kwargs)

    @patch.object(blob_processing_module_api.BlobProcessingModule, "get_by_id")
    def test_get_by_id_called(self, mock_get_by_id):
        """test_get_by_id_called"""
        blob_processing_module_api.delete(**self.mock_kwargs)

        mock_get_by_id.assert_called_with(self.mock_kwargs["blob_module_id"])

    @patch.object(blob_processing_module_api.BlobProcessingModule, "get_by_id")
    def test_delete_called(self, mock_get_by_id):
        """test_delete_called"""
        mock_blob_processing_module = MagicMock()
        mock_get_by_id.return_value = mock_blob_processing_module

        blob_processing_module_api.delete(**self.mock_kwargs)

        mock_blob_processing_module.delete.assert_called_with()

    @patch.object(blob_processing_module_api.BlobProcessingModule, "get_by_id")
    def test_success_returns_delete(self, mock_get_by_id):
        """test_success_returns_delete"""
        mock_blob_processing_module = MagicMock()
        mock_get_by_id.return_value = mock_blob_processing_module
        mock_delete_value = MagicMock()
        mock_blob_processing_module.delete.return_value = mock_delete_value

        self.assertEqual(
            blob_processing_module_api.delete(**self.mock_kwargs),
            mock_delete_value,
        )
