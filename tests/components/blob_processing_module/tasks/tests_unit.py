""" Unit tests for `core_main_app.components.blob_processing_module.api` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.commons.exceptions import ApiError
from core_main_app.components.blob_processing_module import (
    tasks as blob_processing_module_tasks,
)


class TestProcessBlob(TestCase):
    """Unit test for `process_blob` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "blob_module_id": MagicMock(),
            "blob_id": MagicMock(),
            "strategy": MagicMock(),
            "user_id": MagicMock(),
        }

    def test_user_id_not_set_raises_api_error(self):
        """test_user_id_not_set_raises_api_error"""
        self.mock_kwargs["user_id"] = None

        with self.assertRaises(ApiError):
            blob_processing_module_tasks.process_blob(**self.mock_kwargs)

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_user_get_called(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_user_get_called"""
        blob_processing_module_tasks.process_blob(**self.mock_kwargs)

        mock_user_model.objects.get.assert_called_with(
            pk=self.mock_kwargs["user_id"]
        )

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_user_get_fails_error_api_error(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_user_get_fails_error_api_error"""
        mock_user_model.objects.get.side_effect = Exception(
            "mock_user_model_get_exeption"
        )

        with self.assertRaises(ApiError):
            blob_processing_module_tasks.process_blob(**self.mock_kwargs)

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_blob_get_by_id_called(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_blob_get_by_id_called"""
        mock_user = MagicMock()
        mock_user_model.objects.get.return_value = mock_user

        blob_processing_module_tasks.process_blob(**self.mock_kwargs)

        mock_blob_api.get_by_id.assert_called_with(
            self.mock_kwargs["blob_id"], mock_user
        )

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_blob_get_by_id_fails_error_api_error(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_blob_get_by_id_fails_error_api_error"""
        mock_blob_api.get_by_id.side_effect = Exception(
            "mock_blob_api_get_by_id_exeption"
        )

        with self.assertRaises(ApiError):
            blob_processing_module_tasks.process_blob(**self.mock_kwargs)

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_blob_module_get_by_id_called(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_blob_module_get_by_id_called"""
        mock_user = MagicMock()
        mock_user_model.objects.get.return_value = mock_user

        blob_processing_module_tasks.process_blob(**self.mock_kwargs)

        mock_blob_processing_module_api.get_by_id.assert_called_with(
            self.mock_kwargs["blob_module_id"], mock_user
        )

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_blob_module_get_by_id_error_raises_api_error(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_blob_module_get_by_id_error_raises_api_error"""
        mock_blob_processing_module_api.get_by_id.side_effect = Exception(
            "mock_get_by_id_exeption"
        )

        with self.assertRaises(ApiError):
            blob_processing_module_tasks.process_blob(**self.mock_kwargs)

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_blob_module_get_class_called(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_blob_module_get_class_called"""
        mock_module = MagicMock()
        mock_blob_processing_module_api.get_by_id.return_value = mock_module

        blob_processing_module_tasks.process_blob(**self.mock_kwargs)

        mock_module.get_class.assert_called_with()

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_blob_module_get_class_error_raises_api_error(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_blob_module_get_class_error_raises_api_error"""
        mock_module = MagicMock()
        mock_blob_processing_module_api.get_by_id.return_value = mock_module
        mock_module.get_class.side_effect = Exception(
            "mock_module_get_class_exception"
        )

        with self.assertRaises(ApiError):
            blob_processing_module_tasks.process_blob(**self.mock_kwargs)

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_blob_filename_not_matching_blob_module_regexp_raises_api_error(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_blob_filename_not_matching_blob_module_regexp_raises_api_error"""
        mock_re.match.return_value = None

        with self.assertRaises(ApiError):
            blob_processing_module_tasks.process_blob(**self.mock_kwargs)

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_blob_module_class_process_called(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_returns_blob_module_class_process"""
        mock_blob = MagicMock()
        mock_blob_api.get_by_id.return_value = mock_blob

        mock_module = MagicMock()
        mock_blob_processing_module_api.get_by_id.return_value = mock_module
        mock_module_class = MagicMock()
        mock_module.get_class.return_value = mock_module_class

        blob_processing_module_tasks.process_blob(**self.mock_kwargs)

        mock_module_class.process.assert_called_with(
            mock_blob, mock_module.parameters, self.mock_kwargs["strategy"]
        )

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_returns_blob_module_class_process(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_returns_blob_module_class_process"""
        mock_module = MagicMock()
        mock_blob_processing_module_api.get_by_id.return_value = mock_module
        mock_module_class = MagicMock()
        mock_module.get_class.return_value = mock_module_class

        mock_module_class_process_result = MagicMock()
        mock_module_class.process.return_value = (
            mock_module_class_process_result
        )

        self.assertEqual(
            blob_processing_module_tasks.process_blob(**self.mock_kwargs),
            mock_module_class_process_result,
        )

    @patch.object(blob_processing_module_tasks, "User")
    @patch.object(blob_processing_module_tasks, "blob_api")
    @patch.object(blob_processing_module_tasks, "blob_processing_module_api")
    @patch.object(blob_processing_module_tasks, "re")
    def test_blob_module_class_process_error_raises_api_error(
        self,
        mock_re,
        mock_blob_processing_module_api,
        mock_blob_api,
        mock_user_model,
    ):
        """test_blob_module_class_process_error_raises_api_error"""
        mock_module = MagicMock()
        mock_blob_processing_module_api.get_by_id.return_value = mock_module
        mock_module_class = MagicMock()
        mock_module.get_class.return_value = mock_module_class

        mock_module_class.process.side_effect = Exception(
            "mock_module_class_process_exception"
        )

        with self.assertRaises(ApiError):
            blob_processing_module_tasks.process_blob(**self.mock_kwargs)
