""" Unit tests for `core_main_app.system.blob.api` package.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_main_app.system.blob import api as blob_system_api


class TestGetById(TestCase):
    """Unit test for `get_by_id` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"blob_id": MagicMock()}

    @patch.object(blob_system_api, "Blob")
    def test_blob_get_by_id_called(self, mock_blob):
        """test_blob_get_by_id_called"""
        blob_system_api.get_by_id(**self.mock_kwargs)
        mock_blob.get_by_id.assert_called_with(self.mock_kwargs["blob_id"])

    @patch.object(blob_system_api, "Blob")
    def test_returns_blob_get_by_id(self, mock_blob):
        """test_returns_blob_get_by_id"""
        self.assertEqual(
            blob_system_api.get_by_id(**self.mock_kwargs),
            mock_blob.get_by_id(self.mock_kwargs["blob_id"]),
        )
