""" Unit tests for `BlobProcessingModule` from the
`core_main_app.components.blob_processing_module.models` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from django.core.exceptions import ObjectDoesNotExist

from core_main_app.commons.exceptions import DoesNotExist, ModelError
from core_main_app.components.blob_processing_module import (
    models as blob_processing_module_models,
)


class TestGetById(TestCase):
    """Unit tests for `BlobProcessingModule.get_by_id` method."""

    def setUp(self):
        """setUp"""
        self.blob_processing_module = (
            blob_processing_module_models.BlobProcessingModule()
        )
        self.mock_kwargs = {"blob_id": MagicMock()}

    @patch(
        "core_main_app.components.blob_processing_module.models.BlobProcessingModule.objects"
    )
    def test_objects_get_called(self, mock_blob_processing_module_objects):
        """test_objects_get_called"""
        self.blob_processing_module.get_by_id(**self.mock_kwargs)

        mock_blob_processing_module_objects.get.assert_called_with(
            pk=self.mock_kwargs["blob_id"]
        )

    @patch(
        "core_main_app.components.blob_processing_module.models.BlobProcessingModule.objects"
    )
    def test_object_does_not_exist_raises_does_not_exist_exception(
        self, mock_blob_processing_module_objects
    ):
        """test_object_does_not_exist_raises_does_not_exist_exception"""
        mock_blob_processing_module_objects.get.side_effect = (
            ObjectDoesNotExist("mock_dne_exception")
        )

        with self.assertRaises(DoesNotExist):
            self.blob_processing_module.get_by_id(**self.mock_kwargs)

    @patch(
        "core_main_app.components.blob_processing_module.models.BlobProcessingModule.objects"
    )
    def test_exception_raises_model_error(
        self, mock_blob_processing_module_objects
    ):
        """test_exception_raises_model_error"""
        mock_blob_processing_module_objects.get.side_effect = Exception(
            "mock_objects_get_exception"
        )

        with self.assertRaises(ModelError):
            self.blob_processing_module.get_by_id(**self.mock_kwargs)

    @patch(
        "core_main_app.components.blob_processing_module.models.BlobProcessingModule.objects"
    )
    def test_returns_objects_get(self, mock_blob_processing_module_objects):
        """test_returns_objects_get"""
        mock_module_instance = MagicMock()
        mock_blob_processing_module_objects.get.return_value = (
            mock_module_instance
        )

        self.assertEqual(
            self.blob_processing_module.get_by_id(**self.mock_kwargs),
            mock_module_instance,
        )


class TestGetAll(TestCase):
    """Unit tests for `BlobProcessingModule.get_all` method."""

    def setUp(self):
        """setUp"""
        self.blob_processing_module = (
            blob_processing_module_models.BlobProcessingModule()
        )

    @patch(
        "core_main_app.components.blob_processing_module.models.BlobProcessingModule.objects"
    )
    def test_objects_all_called(self, mock_blob_processing_module_objects):
        """test_objects_all_called"""
        self.blob_processing_module.get_all()

        mock_blob_processing_module_objects.all.assert_called_with()

    @patch(
        "core_main_app.components.blob_processing_module.models.BlobProcessingModule.objects"
    )
    def test_returns_objects_all(self, mock_blob_processing_module_objects):
        """test_returns_objects_all"""
        mock_module_list = MagicMock()
        mock_blob_processing_module_objects.all.return_value = mock_module_list

        self.assertEqual(
            self.blob_processing_module.get_all(), mock_module_list
        )
