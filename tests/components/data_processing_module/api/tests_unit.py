""" Unit tests for `core_main_app.components.data_processing_module.api` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.components.data_processing_module import (
    api as data_processing_module_api,
)


class TestGetAll(TestCase):
    """Unit test for `get_all` function."""

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(data_processing_module_api, "DataProcessingModule")
    def test_returns_model_get_all(
        self, mock_data_processing_module, mock_user_is_registered
    ):
        """test_returns_model_get_all"""
        data_processing_module_api.get_all(MagicMock())

        mock_data_processing_module.get_all.assert_called_with()


class TestGetById(TestCase):
    """Unit test for `get_by_id` function."""

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(data_processing_module_api, "DataProcessingModule")
    def test_returns_model_get_by_id(
        self, mock_data_processing_module, mock_user_is_registered
    ):
        """test_returns_model_get_by_id"""
        mock_data_module_id = MagicMock()
        data_processing_module_api.get_by_id(mock_data_module_id, MagicMock())

        mock_data_processing_module.get_by_id.assert_called_with(
            mock_data_module_id
        )


class TestGetAllByDataId(TestCase):
    """Unit test for `get_all_by_data_id` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "data_id": MagicMock(),
            "user": MagicMock(),
            "run_strategy": MagicMock(),
        }

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(data_processing_module_api, "data_api")
    @patch.object(data_processing_module_api, "get_all")
    def test_data_get_by_id_called(
        self, mock_get_all, mock_data_api, mock_user_is_registered
    ):
        """test_data_get_by_id_called"""
        mock_get_all.return_value = MagicMock()

        data_processing_module_api.get_all_by_data_id(**self.mock_kwargs)

        mock_data_api.get_by_id.assert_called_with(
            self.mock_kwargs["data_id"], self.mock_kwargs["user"]
        )

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(data_processing_module_api, "data_api")
    @patch.object(data_processing_module_api, "get_all")
    def test_data_module_get_all_called(
        self, mock_get_all, mock_data_api, mock_user_is_registered
    ):
        """test_data_module_get_all_called"""
        mock_get_all.return_value = MagicMock()

        data_processing_module_api.get_all_by_data_id(**self.mock_kwargs)

        mock_get_all.assert_called_with(self.mock_kwargs["user"])

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(data_processing_module_api, "data_api")
    @patch.object(data_processing_module_api, "get_all")
    def test_run_strategy_null_does_not_filter(
        self, mock_get_all, mock_data_api, mock_user_is_registered
    ):
        """test_run_strategy_null_does_not_filter"""
        self.mock_kwargs["run_strategy"] = None
        mock_data_module_list = MagicMock()
        mock_get_all.return_value = mock_data_module_list

        data_processing_module_api.get_all_by_data_id(**self.mock_kwargs)

        mock_data_module_list.filter.assert_not_called()

    @patch("core_main_app.access_control.api.check_anonymous_access")
    @patch.object(data_processing_module_api, "data_api")
    @patch.object(data_processing_module_api, "get_all")
    def test_run_strategy_not_null_does_filter(
        self, mock_get_all, mock_data_api, mock_user_is_registered
    ):
        """test_run_strategy_not_null_does_filter"""
        mock_data_module_list = MagicMock()
        mock_get_all.return_value = mock_data_module_list

        data_processing_module_api.get_all_by_data_id(**self.mock_kwargs)

        mock_data_module_list.filter.assert_called_with(
            run_strategy_list__contains=self.mock_kwargs["run_strategy"]
        )
