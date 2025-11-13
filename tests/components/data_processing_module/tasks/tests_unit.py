""" Unit tests for `core_main_app.components.data_processing_module.api` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.commons.exceptions import ApiError
from core_main_app.components.data_processing_module import (
    tasks as data_processing_module_tasks,
)


class TestProcessDataWithModule(TestCase):
    """Unit test for `process_data` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "data_module_id": MagicMock(),
            "data_id": MagicMock(),
            "strategy": MagicMock(),
            "user_id": MagicMock(),
        }

    def test_user_id_not_set_raises_api_error(self):
        """test_user_id_not_set_raises_api_error"""
        self.mock_kwargs["user_id"] = None

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_module(
                **self.mock_kwargs
            )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_user_get_called(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_user_get_called"""
        data_processing_module_tasks.process_data_with_module(
            **self.mock_kwargs
        )

        mock_user_model.objects.get.assert_called_with(
            pk=self.mock_kwargs["user_id"]
        )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_user_get_fails_error_api_error(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_user_get_fails_error_api_error"""
        mock_user_model.objects.get.side_effect = Exception(
            "mock_user_model_get_exception"
        )

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_module(
                **self.mock_kwargs
            )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_get_by_id_called(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_get_by_id_called"""
        mock_user = MagicMock()
        mock_user_model.objects.get.return_value = mock_user

        data_processing_module_tasks.process_data_with_module(
            **self.mock_kwargs
        )

        mock_data_api.get_by_id.assert_called_with(
            self.mock_kwargs["data_id"], mock_user
        )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_get_by_id_fails_error_api_error(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_get_by_id_fails_error_api_error"""
        mock_data_api.get_by_id.side_effect = Exception(
            "mock_data_api_get_by_id_exception"
        )

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_module(
                **self.mock_kwargs
            )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_get_by_id_called(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_module_get_by_id_called"""
        mock_user = MagicMock()
        mock_user_model.objects.get.return_value = mock_user

        data_processing_module_tasks.process_data_with_module(
            **self.mock_kwargs
        )

        mock_data_processing_module_api.get_by_id.assert_called_with(
            self.mock_kwargs["data_module_id"], mock_user
        )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_get_by_id_error_raises_api_error(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_module_get_by_id_error_raises_api_error"""
        mock_data_processing_module_api.get_by_id.side_effect = Exception(
            "mock_get_by_id_exception"
        )

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_module(
                **self.mock_kwargs
            )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_get_class_called(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_module_get_class_called"""
        mock_module = MagicMock()
        mock_data_processing_module_api.get_by_id.return_value = mock_module

        data_processing_module_tasks.process_data_with_module(
            **self.mock_kwargs
        )

        mock_module.get_class.assert_called_with()

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_get_class_error_raises_api_error(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_module_get_class_error_raises_api_error"""
        mock_module = MagicMock()
        mock_data_processing_module_api.get_by_id.return_value = mock_module
        mock_module.get_class.side_effect = Exception(
            "mock_module_get_class_exception"
        )

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_module(
                **self.mock_kwargs
            )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_class_process_called(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_returns_data_module_class_process"""
        mock_data = MagicMock()
        mock_data_api.get_by_id.return_value = mock_data

        mock_module = MagicMock()
        mock_data_processing_module_api.get_by_id.return_value = mock_module
        mock_module_class = MagicMock()
        mock_module.get_class.return_value = mock_module_class

        data_processing_module_tasks.process_data_with_module(
            **self.mock_kwargs
        )

        mock_module_class.process.assert_called_with(
            mock_data, mock_module.parameters, self.mock_kwargs["strategy"]
        )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_returns_data_module_class_process(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_returns_data_module_class_process"""
        mock_module = MagicMock()
        mock_data_processing_module_api.get_by_id.return_value = mock_module
        mock_module_class = MagicMock()
        mock_module.get_class.return_value = mock_module_class

        mock_module_class_process_result = MagicMock()
        mock_module_class.process.return_value = (
            mock_module_class_process_result
        )

        self.assertEqual(
            data_processing_module_tasks.process_data_with_module(
                **self.mock_kwargs
            ),
            mock_module_class_process_result,
        )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_class_process_error_raises_api_error(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_module_class_process_error_raises_api_error"""
        mock_module = MagicMock()
        mock_data_processing_module_api.get_by_id.return_value = mock_module
        mock_module_class = MagicMock()
        mock_module.get_class.return_value = mock_module_class

        mock_module_class.process.side_effect = Exception(
            "mock_module_class_process_exception"
        )

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_module(
                **self.mock_kwargs
            )


class TestProcessDataWithAllModules(TestCase):
    """Unit test for `process_data_with_all_modules` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "data_id": MagicMock(),
            "strategy": MagicMock(),
            "user_id": MagicMock(),
        }

    def test_user_id_not_set_raises_api_error(self):
        """test_user_id_not_set_raises_api_error"""
        self.mock_kwargs["user_id"] = None

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_all_modules(
                **self.mock_kwargs
            )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_user_get_called(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_user_get_called"""
        data_processing_module_tasks.process_data_with_all_modules(
            **self.mock_kwargs
        )

        mock_user_model.objects.get.assert_called_with(
            pk=self.mock_kwargs["user_id"]
        )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_user_get_fails_error_api_error(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_user_get_fails_error_api_error"""
        mock_user_model.objects.get.side_effect = Exception(
            "mock_user_model_get_exception"
        )

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_all_modules(
                **self.mock_kwargs
            )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_get_by_id_called(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_get_by_id_called"""
        mock_user = MagicMock()
        mock_user_model.objects.get.return_value = mock_user

        data_processing_module_tasks.process_data_with_all_modules(
            **self.mock_kwargs
        )

        mock_data_api.get_by_id.assert_called_with(
            self.mock_kwargs["data_id"], mock_user
        )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_get_by_id_fails_error_api_error(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_get_by_id_fails_error_api_error"""
        mock_data_api.get_by_id.side_effect = Exception(
            "mock_data_api_get_by_id_exception"
        )

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_all_modules(
                **self.mock_kwargs
            )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_get_all_called(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_module_get_all_called"""
        mock_user = MagicMock()
        mock_user_model.objects.get.return_value = mock_user

        data_processing_module_tasks.process_data_with_all_modules(
            **self.mock_kwargs
        )

        mock_data_processing_module_api.get_all.assert_called_with(mock_user)

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_get_all_error_raises_api_error(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_module_get_by_id_error_raises_api_error"""
        mock_data_processing_module_api.get_all.side_effect = Exception(
            "mock_get_all_exception"
        )

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_all_modules(
                **self.mock_kwargs
            )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_get_class_called(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_module_get_class_called"""
        mock_data = MagicMock()
        mock_data.template.filename = "schema.json"
        mock_data_api.get_by_id.return_value = mock_data

        mock_module = MagicMock()
        mock_module.template_filename_regexp = ".*"
        mock_module_qs = MagicMock()
        mock_module_qs.filter.return_value = [mock_module]
        mock_data_processing_module_api.get_all.return_value = mock_module_qs

        data_processing_module_tasks.process_data_with_all_modules(
            **self.mock_kwargs
        )

        mock_module.get_class.assert_called_with()

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_get_class_error_raises_api_error(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_module_get_class_error_raises_api_error"""
        mock_data = MagicMock()
        mock_data.template.filename = "schema.json"
        mock_data_api.get_by_id.return_value = mock_data

        mock_module = MagicMock()
        mock_module.template_filename_regexp = ".*"
        mock_module_qs = MagicMock()
        mock_module_qs.filter.return_value = [mock_module]
        mock_data_processing_module_api.get_all.return_value = mock_module_qs

        mock_module.get_class.side_effect = Exception(
            "mock_module_get_class_exception"
        )

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_all_modules(
                **self.mock_kwargs
            )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_class_process_called(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_returns_data_module_class_process"""
        mock_data = MagicMock()
        mock_data.template.filename = "schema.json"
        mock_data_api.get_by_id.return_value = mock_data

        mock_module = MagicMock()
        mock_module.template_filename_regexp = ".*"
        mock_module_qs = MagicMock()
        mock_module_qs.filter.return_value = [mock_module]
        mock_data_processing_module_api.get_all.return_value = mock_module_qs

        mock_module_class = MagicMock()
        mock_module.get_class.return_value = mock_module_class

        data_processing_module_tasks.process_data_with_all_modules(
            **self.mock_kwargs
        )

        mock_module_class.process.assert_called_with(
            mock_data, mock_module.parameters, self.mock_kwargs["strategy"]
        )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_returns_data_module_class_process(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_returns_data_module_class_process"""
        mock_data = MagicMock()
        mock_data.template.filename = "schema.json"
        mock_data_api.get_by_id.return_value = mock_data

        mock_module = MagicMock()
        mock_module.template_filename_regexp = ".*"
        mock_module_qs = MagicMock()
        mock_module_qs.filter.return_value = [mock_module]
        mock_data_processing_module_api.get_all.return_value = mock_module_qs

        mock_module_class = MagicMock()
        mock_module.get_class.return_value = mock_module_class

        mock_module_class_process_result = MagicMock()
        mock_module_class.process.return_value = (
            mock_module_class_process_result
        )

        self.assertEqual(
            data_processing_module_tasks.process_data_with_all_modules(
                **self.mock_kwargs
            ),
            mock_module_class_process_result,
        )

    @patch.object(data_processing_module_tasks, "User")
    @patch.object(data_processing_module_tasks, "data_api")
    @patch.object(data_processing_module_tasks, "data_processing_module_api")
    @patch.object(data_processing_module_tasks, "check_can_write")
    def test_data_module_class_process_error_raises_api_error(
        self,
        mock_check_can_write,
        mock_data_processing_module_api,
        mock_data_api,
        mock_user_model,
    ):
        """test_data_module_class_process_error_raises_api_error"""
        mock_data = MagicMock()
        mock_data.template.filename = "schema.json"
        mock_data_api.get_by_id.return_value = mock_data

        mock_module = MagicMock()
        mock_module.template_filename_regexp = ".*"
        mock_module_qs = MagicMock()
        mock_module_qs.filter.return_value = [mock_module]
        mock_data_processing_module_api.get_all.return_value = mock_module_qs

        mock_module_class = MagicMock()
        mock_module.get_class.return_value = mock_module_class

        mock_module_class_process_result = MagicMock()
        mock_module_class.process.return_value = (
            mock_module_class_process_result
        )

        mock_module_class.process.side_effect = Exception(
            "mock_module_class_process_exception"
        )

        with self.assertRaises(ApiError):
            data_processing_module_tasks.process_data_with_all_modules(
                **self.mock_kwargs
            )
