""" Unit test Blob
"""

from unittest.case import TestCase
from unittest.mock import patch

from django.contrib.auth.models import User
from tests.components.data.tests_unit import (
    _create_blob,
    _create_data,
    _get_template,
)

from core_main_app.components.blob import api as blob_api
from core_main_app.utils.tests_tools.MockUser import create_mock_user


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


class TestBlobMetadata(TestCase):
    """Test Blob Metadata"""

    def test_blob_metadata_returns_list_of_data(self):
        """test_blob_metadata_returns_list_of_data

        Returns:

        """
        # Arrange
        blob = _create_blob(user_id="2")
        blob.save()
        template = _get_template()
        template.save()
        data = _create_data(
            data_id=1,
            template=template,
            user_id="2",
            title="new_title",
            content="<tag></tag>",
            blob=blob,
        )
        data.save()
        blob._metadata.set([data])
        user = create_mock_user("2", is_superuser=True)
        # Act
        metadata = blob.metadata(user=user)
        # Assert
        self.assertEqual(list(metadata), [data])

    def test_blob_metadata_returns_empty_list_if_not_set(self):
        """test_blob_metadata_returns_none_if_not_set

        Returns:

        """
        # Arrange
        blob = _create_blob(user_id="2")
        blob.save()
        user = create_mock_user("2", is_superuser=True)
        # Act
        metadata = blob.metadata(user=user)
        # Assert
        self.assertEqual(list(metadata), [])


class TestBlobOwnerName(TestCase):
    """Test Blob Owner Name"""

    @patch.object(User, "objects")
    def test_blob_owner_name(self, user_objects):
        """test_blob_owner_name

        Returns:

        """
        # Arrange
        user = create_mock_user(user_id="2")
        user.username = "user"
        user_objects.get.return_value = user

        blob = _create_blob(user_id="2")

        # Assert
        self.assertEqual(blob.owner_name, user.username)
