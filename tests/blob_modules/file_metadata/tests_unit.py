""" Unit tests for `FileMetadataBlobProcessing` class.
"""

import json
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.blob_modules import file_metadata


class TestFileMetadataBlobProcessingProcessOnRead(TestCase):
    def setUp(self):
        self.blob_processing_module = (
            file_metadata.FileMetadataBlobProcessing()
        )
        self.mock_kwargs = {
            "blob": MagicMock(),
            "blob_module_params": MagicMock(),
        }

    def test_raises_not_implmented(self):
        with self.assertRaises(NotImplementedError):
            self.blob_processing_module._process_on_read(**self.mock_kwargs)


class TestFileMetadataBlobProcessingProcessOnUpdate(TestCase):
    def setUp(self):
        self.blob_processing_module = (
            file_metadata.FileMetadataBlobProcessing()
        )
        self.mock_kwargs = {
            "blob": MagicMock(),
            "blob_module_params": MagicMock(),
        }

    def test_raises_not_implmented(self):
        with self.assertRaises(NotImplementedError):
            self.blob_processing_module._process_on_update(**self.mock_kwargs)


class TestFileMetadataBlobProcessingProcessOnDelete(TestCase):
    def setUp(self):
        self.blob_processing_module = (
            file_metadata.FileMetadataBlobProcessing()
        )
        self.mock_kwargs = {
            "blob": MagicMock(),
            "blob_module_params": MagicMock(),
        }

    def test_raises_not_implmented(self):
        with self.assertRaises(NotImplementedError):
            self.blob_processing_module._process_on_delete(**self.mock_kwargs)


class TestFileMetadataBlobProcessingProcessOnCreate(TestCase):
    def setUp(self):
        self.blob_processing_module = (
            file_metadata.FileMetadataBlobProcessing()
        )

        self.mock_kwargs = {
            "blob": MagicMock(),
            "blob_module_params": MagicMock(),
        }

    def test_raises_not_implmented(self):
        with self.assertRaises(NotImplementedError):
            self.blob_processing_module._process_on_create(**self.mock_kwargs)


class TestFileMetadataBlobProcessingProcessOnDemand(TestCase):
    def setUp(self):
        self.blob_processing_module = (
            file_metadata.FileMetadataBlobProcessing()
        )

        self.mock_blob = MagicMock()
        self.mock_blob.filename = "mock_blob.ext"
        self.mock_blob.size = 42

        self.mock_kwargs = {
            "blob": self.mock_blob,
            "blob_module_params": MagicMock(),
        }

    @patch.object(file_metadata, "system_api")
    @patch.object(file_metadata, "Data")
    def test_get_template_by_id_called(self, mock_data, mock_system_api):
        self.blob_processing_module._process_on_demand(**self.mock_kwargs)

        mock_system_api.get_template_by_id.assert_called_with(
            self.mock_kwargs["blob_module_params"]["template_pk"]
        )

    @patch.object(file_metadata, "system_api")
    @patch.object(file_metadata, "Data")
    def test_data_instantiated(self, mock_data, mock_system_api):
        mock_template = MagicMock()
        mock_system_api.get_template_by_id.return_value = mock_template

        self.blob_processing_module._process_on_demand(**self.mock_kwargs)

        mock_data.assert_called_with(
            title=self.mock_blob.filename,
            template=mock_template,
            user_id=str(self.mock_blob.user_id),
            content=json.dumps(
                {
                    "filename": self.mock_blob.filename,
                    "size": self.mock_blob.size,
                }
            ),
        )

    @patch.object(file_metadata, "system_api")
    @patch.object(file_metadata, "Data")
    def test_upsert_data_called(self, mock_data, mock_system_api):
        mock_data_instance = MagicMock()
        mock_data.return_value = mock_data_instance

        self.blob_processing_module._process_on_demand(**self.mock_kwargs)

        mock_system_api.upsert_data.assert_called_with(mock_data_instance)

    @patch.object(file_metadata, "blob_system_api")
    @patch.object(file_metadata, "system_api")
    @patch.object(file_metadata, "Data")
    def test_add_metadata_called(
        self, mock_data, mock_system_api, mock_blob_system_api
    ):
        mock_data_instance = MagicMock()
        mock_data.return_value = mock_data_instance

        self.blob_processing_module._process_on_demand(**self.mock_kwargs)

        mock_blob_system_api.add_metadata.assert_called_with(
            self.mock_blob, mock_data_instance
        )

    @patch.object(file_metadata, "blob_system_api")
    @patch.object(file_metadata, "system_api")
    @patch.object(file_metadata, "Data")
    def test_successful_execution_returns_data(
        self, mock_data, mock_system_api, mock_blob_system_api
    ):
        mock_data_instance = MagicMock()
        mock_data.return_value = mock_data_instance

        self.assertEqual(
            self.blob_processing_module._process_on_demand(**self.mock_kwargs),
            mock_data_instance,
        )
