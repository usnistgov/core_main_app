""" Int test Blob
"""

from tests.components.blob.fixtures.fixtures import (
    BlobFixtures,
    AccessControlBlobFixture,
)

from core_main_app.commons import exceptions
from core_main_app.components.blob.models import Blob
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)

fixture_blob = BlobFixtures()
fixture_blob_workspace = AccessControlBlobFixture()


class TestBlobGetAll(MongoIntegrationBaseTestCase):
    """TestBlobGetAll"""

    fixture = fixture_blob

    def test_blob_get_all_return_collection_of_blob(self):
        """test_blob_get_all_return_collection_of_blob

        Returns:

        """
        # Act
        result = Blob.get_all()
        # Assert
        self.assertTrue(all(isinstance(item, Blob) for item in result))

    def test_blob_get_all_return_objects_blob_in_collection(self):
        """test_blob_get_all_return_objects_blob_in_collection

        Returns:

        """
        # Act
        result = Blob.get_all()
        # Assert
        self.assertTrue(len(self.fixture.blob_collection) == result.count())


class TestBlobGetById(MongoIntegrationBaseTestCase):
    """TestBlobGetById"""

    fixture = fixture_blob

    def test_blob_get_by_id_raises_does_not_exist_error_if_not_found(self):
        """test_blob_get_by_id_raises_does_not_exist_error_if_not_found

        Returns:

        """
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            Blob.get_by_id(-1)

    def test_blob_get_by_id_return_blob_if_found(self):
        """test_blob_get_by_id_return_blob_if_found

        Returns:

        """
        # Act
        result = Blob.get_by_id(self.fixture.blob_1.id)
        # Assert
        self.assertEqual(result, self.fixture.blob_1)


class TestBlobGetAllByUserId(MongoIntegrationBaseTestCase):
    """TestBlobGetAllByUserId"""

    fixture = fixture_blob

    def test_blob_get_all_by_user_id_return_collection_of_blob_from_user(self):
        """test_blob_get_all_by_user_id_return_collection_of_blob_from_user

        Returns:

        """
        # Arrange
        user_id = 1
        # Act
        result = Blob.get_all_by_user_id(user_id)
        # Assert
        self.assertTrue(all(item.user_id == str(user_id) for item in result))

    def test_blob_get_all_by_user_id_return_empty_collection_of_blob_from_user_with_no_associated_blob(
        self,
    ):
        """test_blob_get_all_by_user_id_return_empty_collection_of_blob_from_user_with_no_associated_blob

        Returns:

        """
        # Arrange
        user_id = 800
        # Act
        result = Blob.get_all_by_user_id(user_id)
        # Assert
        self.assertTrue(result.count() == 0)


class TestBlobGetAllByWorkspace(MongoIntegrationBaseTestCase):
    """TestBlobGetAllByWorkspace"""

    fixture = fixture_blob_workspace

    def test_blob_get_all_by_workspace_return_collection_of_blob_from_user(self):
        """test_blob_get_all_by_workspace_return_collection_of_blob_from_user

        Returns:

        """
        # Act
        result = Blob.get_all_by_workspace(self.fixture.workspace_1)
        # Assert
        self.assertTrue(
            all(item.user_id == str(self.fixture.workspace_1.owner) for item in result)
        )

    def test_blob_get_all_by_workspace_return_empty_collection_of_blob_from_empty_workspace(
        self,
    ):
        """test_blob_get_all_by_workspace_return_empty_collection_of_blob_from_empty_workspace

        Returns:

        """
        # Act
        result = Blob.get_all_by_workspace(self.fixture.workspace_without_data)
        # Assert
        self.assertTrue(result.count() == 0)


class TestBlobGetAllByListWorkspace(MongoIntegrationBaseTestCase):
    """TestBlobGetAllByListWorkspace"""

    fixture = fixture_blob_workspace

    def test_blob_get_all_by_workspace_return_collection_of_blob_from_user(self):
        """test_blob_get_all_by_workspace_return_collection_of_blob_from_user

        Returns:

        """
        # Act
        result = Blob.get_all_by_list_workspace(
            [self.fixture.workspace_1, self.fixture.workspace_2]
        )
        # Assert
        self.assertTrue(
            all(
                item.user_id == str(self.fixture.workspace_1.owner)
                or item.user_id == str(self.fixture.workspace_2.owner)
                for item in result
            )
        )

    def test_blob_get_all_by_workspace_return_empty_collection_of_blob_from_empty_workspace(
        self,
    ):
        """test_blob_get_all_by_workspace_return_empty_collection_of_blob_from_empty_workspace

        Returns:

        """
        # Act
        result = Blob.get_all_by_list_workspace([self.fixture.workspace_without_data])
        # Assert
        self.assertTrue(result.count() == 0)
