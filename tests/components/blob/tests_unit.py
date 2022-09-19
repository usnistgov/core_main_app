""" Unit test Blob
"""

from unittest.case import TestCase
from core_main_app.components.blob import api as blob_api


class TestBlobGetNone(TestCase):
    """Test Blob Get None"""

    def test_blob_get_none_returns_empty_list(self):
        """test_blob_get_none_returns_empty_list

        Args:

        Returns:

        """
        # Act
        result = blob_api.get_none()

        # Assert
        self.assertEqual(len(result), 0)
