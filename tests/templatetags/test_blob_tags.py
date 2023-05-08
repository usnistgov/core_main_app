""" Unit tests of blob templatetag
"""
from unittest.case import TestCase
from unittest.mock import MagicMock

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.templatetags.blob_tags import blob_metadata, data_blob
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestBlobMetadata(TestCase):
    """Test blob metadata"""

    def test_blob_metadata_returns_metadata(self):
        """test_blob_metadata_returns_metadata

        Returns:

        """
        mock_data = MagicMock()
        mock_blob = MagicMock()
        mock_blob.metadata.return_value = [mock_data]
        mock_user = create_mock_user("1")
        result = blob_metadata(mock_blob, mock_user)
        self.assertEqual(result, [mock_data])

    def test_blob_metadata_with_acl_error_returns_none(self):
        """test_blob_metadata_with_acl_error_returns_none

        Returns:

        """
        mock_blob = MagicMock()
        mock_blob.metadata.side_effect = AccessControlError("error")
        mock_user = create_mock_user("1")
        result = blob_metadata(mock_blob, mock_user)
        self.assertIsNone(result)


class TestDataBlob(TestCase):
    """Test data blob"""

    def test_data_blob_returns_blob(self):
        """test_data_blob_returns_blob

        Returns:

        """
        mock_data = MagicMock()
        mock_blob = MagicMock()
        mock_data.blob.return_value = mock_blob
        mock_user = create_mock_user("1")
        result = data_blob(mock_data, mock_user)
        self.assertEqual(result, mock_blob)

    def test_data_blob_with_acl_error_returns_none(self):
        """test_data_blob_with_acl_error_returns_none

        Returns:

        """
        mock_data = MagicMock()
        mock_data.blob.side_effect = AccessControlError("error")
        mock_user = create_mock_user("1")
        result = data_blob(mock_data, mock_user)
        self.assertIsNone(result)
