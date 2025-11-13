""" Unit tests for `DataProcessingModule` from the
`core_main_app.components.data_processing_module.models` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from django.core.exceptions import ObjectDoesNotExist

from core_main_app.commons.exceptions import DoesNotExist, ModelError
from core_main_app.components.data_processing_module import (
    models as data_processing_module_models,
)


class TestGetById(TestCase):
    """Unit tests for `DataProcessingModule.get_by_id` method."""

    def setUp(self):
        """setUp"""
        self.data_processing_module = (
            data_processing_module_models.DataProcessingModule()
        )
        self.mock_kwargs = {"data_module_id": MagicMock()}

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_objects_get_called(self, mock_data_processing_module_objects):
        """test_objects_get_called"""
        self.data_processing_module.get_by_id(**self.mock_kwargs)

        mock_data_processing_module_objects.get.assert_called_with(
            pk=self.mock_kwargs["data_module_id"]
        )

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_object_does_not_exist_raises_does_not_exist_exception(
        self, mock_data_processing_module_objects
    ):
        """test_object_does_not_exist_raises_does_not_exist_exception"""
        mock_data_processing_module_objects.get.side_effect = (
            ObjectDoesNotExist("mock_dne_exception")
        )

        with self.assertRaises(DoesNotExist):
            self.data_processing_module.get_by_id(**self.mock_kwargs)

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_exception_raises_model_error(
        self, mock_data_processing_module_objects
    ):
        """test_exception_raises_model_error"""
        mock_data_processing_module_objects.get.side_effect = Exception(
            "mock_objects_get_exception"
        )

        with self.assertRaises(ModelError):
            self.data_processing_module.get_by_id(**self.mock_kwargs)

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_returns_objects_get(self, mock_data_processing_module_objects):
        """test_returns_objects_get"""
        mock_module_instance = MagicMock()
        mock_data_processing_module_objects.get.return_value = (
            mock_module_instance
        )

        self.assertEqual(
            self.data_processing_module.get_by_id(**self.mock_kwargs),
            mock_module_instance,
        )


class TestGetAll(TestCase):
    """Unit tests for `DataProcessingModule.get_all` method."""

    def setUp(self):
        """setUp"""
        self.data_processing_module = (
            data_processing_module_models.DataProcessingModule()
        )

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_objects_all_called(self, mock_data_processing_module_objects):
        """test_objects_all_called"""
        self.data_processing_module.get_all()

        mock_data_processing_module_objects.all.assert_called_with()

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_returns_objects_all(self, mock_data_processing_module_objects):
        """test_returns_objects_all"""
        mock_module_list = MagicMock()
        mock_data_processing_module_objects.all.return_value = mock_module_list

        self.assertEqual(
            self.data_processing_module.get_all(), mock_module_list
        )
