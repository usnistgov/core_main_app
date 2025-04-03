""" Unit tests for `FileMetadataBlobProcessing` class.
"""

import json
from core_main_app.utils import datetime
from datetime import timedelta
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.blob_modules import file_metadata
from core_main_app.blob_modules.file_metadata import FileMetadataBlobProcessing
from core_main_app.commons.exceptions import CoreError


class TestFileMetadataBlobProcessingProcessOnRead(TestCase):
    def setUp(self):
        self.blob_processing_module = (
            file_metadata.FileMetadataBlobProcessing()
        )

        self.mock_blob = MagicMock()
        self.mock_blob.filename = "mock_blob.ext"
        self.mock_blob.size = 42
        self.mock_blob.pk = 1
        self.mock_blob.checksum = "abcedf"

        self.mock_kwargs = {
            "blob": self.mock_blob,
            "blob_module_params": MagicMock(),
        }

    def test_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.blob_processing_module._process_on_read(**self.mock_kwargs)


class TestFileMetadataBlobProcessingProcessOnUpdate(TestCase):
    def setUp(self):
        self.blob_processing_module = (
            file_metadata.FileMetadataBlobProcessing()
        )

        self.mock_blob = MagicMock()
        self.mock_blob.filename = "mock_blob.ext"
        self.mock_blob.size = 42
        self.mock_blob.pk = 1
        self.mock_blob.checksum = "abcedf"

        self.mock_kwargs = {
            "blob": self.mock_blob,
            "blob_module_params": MagicMock(),
        }

    @patch.object(file_metadata, "Data")
    def test_too_many_metadata_raises_core_error(
        self,
        mock_data,
    ):
        mock_data_instance = MagicMock()
        mock_data_instance.title = (
            FileMetadataBlobProcessing._get_metadata_title(
                self.mock_blob.filename
            )
        )
        mock_data.objects.filter.return_value = [
            mock_data_instance,
            mock_data_instance,
        ]

        with self.assertRaises(CoreError):
            self.blob_processing_module._process_on_update(**self.mock_kwargs)

    @patch.object(file_metadata, "system_api")
    @patch.object(file_metadata, "Data")
    def test_metadata_updated(self, mock_data, mock_system_api):
        mock_data_instance = MagicMock()
        mock_data_instance.title = (
            FileMetadataBlobProcessing._get_metadata_title(
                self.mock_blob.filename
            )
        )
        initial_date = datetime.datetime_to_utc_datetime_iso8601(
            datetime.datetime_now() - timedelta(hours=1)
        )
        mock_data_instance.dict_content = {
            "dates": {
                "creation_date": initial_date,
                "modification_date": initial_date,
            }
        }
        mock_data_instance.get_dict_content.return_value = (
            mock_data_instance.dict_content
        )
        mock_data.objects.filter.return_value = [
            mock_data_instance,
        ]

        self.blob_processing_module._process_on_update(**self.mock_kwargs)

        self.assertNotEqual(
            json.loads(mock_system_api.upsert_data.call_args[0][0].content)[
                "dates"
            ]["creation_date"],
            json.loads(mock_system_api.upsert_data.call_args[0][0].content)[
                "dates"
            ]["modification_date"],
        )


class TestFileMetadataBlobProcessingProcessOnDelete(TestCase):
    def setUp(self):
        self.blob_processing_module = (
            file_metadata.FileMetadataBlobProcessing()
        )

        self.mock_blob = MagicMock()
        self.mock_blob.filename = "mock_blob.ext"
        self.mock_blob.size = 42
        self.mock_blob.pk = 1
        self.mock_blob.checksum = "abcedf"

        self.mock_kwargs = {
            "blob": self.mock_blob,
            "blob_module_params": MagicMock(),
        }

    @patch.object(file_metadata, "Data")
    def test_too_many_metadata_raises_core_error(
        self,
        mock_data,
    ):
        mock_data_instance = MagicMock()
        mock_data_instance.title = (
            FileMetadataBlobProcessing._get_metadata_title(
                self.mock_blob.filename
            )
        )
        mock_data.objects.filter.return_value = [
            mock_data_instance,
            mock_data_instance,
        ]

        with self.assertRaises(CoreError):
            self.blob_processing_module._process_on_delete(**self.mock_kwargs)

    @patch.object(file_metadata, "Data")
    def test_no_metadata_does_nothing(self, mock_data):
        mock_data_instance = MagicMock()

        mock_data.objects.filter.return_value = []

        self.blob_processing_module._process_on_delete(**self.mock_kwargs)

        self.assertFalse(mock_data_instance.delete.called)

    @patch.object(file_metadata, "Data")
    def test_metadata_deleted(self, mock_data):
        mock_data_instance = MagicMock()
        mock_data_instance.title = (
            FileMetadataBlobProcessing._get_metadata_title(
                self.mock_blob.filename
            )
        )
        mock_data.objects.filter.return_value = [
            mock_data_instance,
        ]

        self.blob_processing_module._process_on_delete(**self.mock_kwargs)

        self.assertTrue(mock_data_instance.delete.called)


class TestFileMetadataBlobProcessingProcessOnCreate(TestCase):
    def setUp(self):
        self.blob_processing_module = (
            file_metadata.FileMetadataBlobProcessing()
        )

        self.mock_blob = MagicMock()
        self.mock_blob.filename = "mock_blob.ext"
        self.mock_blob.size = 42
        self.mock_blob.pk = 1
        self.mock_blob.checksum = "abcedf"

        self.mock_kwargs = {
            "blob": self.mock_blob,
            "blob_module_params": MagicMock(),
        }

    @patch.object(file_metadata, "system_api")
    @patch.object(file_metadata, "Data")
    def test_get_template_by_id_called(self, mock_data, mock_system_api):
        self.blob_processing_module._process_on_create(**self.mock_kwargs)

        mock_system_api.get_template_by_id.assert_called_with(
            self.mock_kwargs["blob_module_params"]["template_pk"]
        )

    @patch.object(file_metadata, "system_api")
    @patch.object(file_metadata, "Data")
    def test_data_instantiated(self, mock_data, mock_system_api):
        mock_template = MagicMock()
        mock_system_api.get_template_by_id.return_value = mock_template

        self.blob_processing_module._process_on_create(**self.mock_kwargs)

        self.assertEqual(
            mock_data.call_args.kwargs["title"],
            FileMetadataBlobProcessing._get_metadata_title(
                self.mock_blob.filename
            ),
        )
        self.assertEqual(mock_data.call_args.kwargs["template"], mock_template)
        self.assertEqual(
            mock_data.call_args.kwargs["user_id"], str(self.mock_blob.user_id)
        )
        self.assertEqual(
            json.loads(mock_data.call_args.kwargs["content"])["filename"],
            self.mock_blob.filename,
        )
        self.assertEqual(
            json.loads(mock_data.call_args.kwargs["content"])["checksum"],
            self.mock_blob.checksum,
        )
        self.assertEqual(
            json.loads(mock_data.call_args.kwargs["content"])["size"],
            self.mock_blob.size,
        )
        self.assertEqual(
            json.loads(mock_data.call_args.kwargs["content"])["url"],
            FileMetadataBlobProcessing._get_blob_detail_url(self.mock_blob.pk),
        )
        self.assertTrue(
            "dates" in json.loads(mock_data.call_args.kwargs["content"])
        )
        self.assertEqual(
            json.loads(mock_data.call_args.kwargs["content"])["dates"][
                "creation_date"
            ],
            json.loads(mock_data.call_args.kwargs["content"])["dates"][
                "modification_date"
            ],
        )

    @patch.object(file_metadata, "system_api")
    @patch.object(file_metadata, "Data")
    def test_upsert_data_called(self, mock_data, mock_system_api):
        mock_data_instance = MagicMock()
        mock_data.return_value = mock_data_instance

        self.blob_processing_module._process_on_create(**self.mock_kwargs)

        mock_system_api.upsert_data.assert_called_with(mock_data_instance)

    @patch.object(file_metadata, "blob_system_api")
    @patch.object(file_metadata, "system_api")
    @patch.object(file_metadata, "Data")
    def test_add_metadata_called(
        self, mock_data, mock_system_api, mock_blob_system_api
    ):
        mock_data_instance = MagicMock()
        mock_data.return_value = mock_data_instance

        self.blob_processing_module._process_on_create(**self.mock_kwargs)

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
            self.blob_processing_module._process_on_create(**self.mock_kwargs),
            mock_data_instance,
        )


class TestFileMetadataBlobProcessingProcessOnDemand(TestCase):
    def setUp(self):
        self.blob_processing_module = (
            file_metadata.FileMetadataBlobProcessing()
        )

        self.mock_blob = MagicMock()
        self.mock_blob.filename = "mock_blob.ext"
        self.mock_blob.size = 42
        self.mock_blob.pk = 1
        self.mock_blob.checksum = "abcedf"

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

        self.assertEqual(
            mock_data.call_args.kwargs["title"],
            FileMetadataBlobProcessing._get_metadata_title(
                self.mock_blob.filename
            ),
        )
        self.assertEqual(mock_data.call_args.kwargs["template"], mock_template)
        self.assertEqual(
            mock_data.call_args.kwargs["user_id"], str(self.mock_blob.user_id)
        )
        self.assertEqual(
            json.loads(mock_data.call_args.kwargs["content"])["filename"],
            self.mock_blob.filename,
        )
        self.assertEqual(
            json.loads(mock_data.call_args.kwargs["content"])["checksum"],
            self.mock_blob.checksum,
        )
        self.assertEqual(
            json.loads(mock_data.call_args.kwargs["content"])["size"],
            self.mock_blob.size,
        )
        self.assertEqual(
            json.loads(mock_data.call_args.kwargs["content"])["url"],
            FileMetadataBlobProcessing._get_blob_detail_url(self.mock_blob.pk),
        )
        self.assertTrue(
            "dates" in json.loads(mock_data.call_args.kwargs["content"])
        )
        self.assertEqual(
            json.loads(mock_data.call_args.kwargs["content"])["dates"][
                "creation_date"
            ],
            json.loads(mock_data.call_args.kwargs["content"])["dates"][
                "modification_date"
            ],
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
