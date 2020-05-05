""" Int test Blob
"""
from bson.objectid import ObjectId

from core_main_app.commons import exceptions
from core_main_app.components.blob.models import Blob
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from tests.components.blob.fixtures.fixtures import (
    BlobFixtures,
    AccessControlBlobFixture,
)

fixture_blob = BlobFixtures()
fixture_blob_workspace = AccessControlBlobFixture()


class TestBlobGetAll(MongoIntegrationBaseTestCase):

    fixture = fixture_blob

    def test_blob_get_all_return_collection_of_blob(self):
        # Act
        result = Blob.get_all()
        # Assert
        self.assertTrue(all(isinstance(item, Blob) for item in result))

    def test_blob_get_all_return_objects_blob_in_collection(self):
        # Act
        result = Blob.get_all()
        # Assert
        self.assertTrue(len(self.fixture.blob_collection) == result.count())


class TestBlobGetById(MongoIntegrationBaseTestCase):

    fixture = fixture_blob

    def test_blob_get_by_id_raises_does_not_exist_error_if_not_found(self):
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            Blob.get_by_id(ObjectId())

    def test_blob_get_by_id_return_blob_if_found(self):
        # Act
        result = Blob.get_by_id(self.fixture.blob_1.id)
        # Assert
        self.assertEqual(result, self.fixture.blob_1)


class TestBlobGetAllByUserId(MongoIntegrationBaseTestCase):

    fixture = fixture_blob

    def test_blob_get_all_by_user_id_return_collection_of_blob_from_user(self):
        # Arrange
        user_id = 1
        # Act
        result = Blob.get_all_by_user_id(user_id)
        # Assert
        self.assertTrue(all(item.user_id == str(user_id) for item in result))

    def test_blob_get_all_by_user_id_return_empty_collection_of_blob_from_user_with_no_associated_blob(
        self,
    ):
        # Arrange
        user_id = 800
        # Act
        result = Blob.get_all_by_user_id(user_id)
        # Assert
        self.assertTrue(result.count() == 0)


class TestBlobGetAllByWorkspace(MongoIntegrationBaseTestCase):

    fixture = fixture_blob_workspace

    def test_blob_get_all_by_workspace_return_collection_of_blob_from_user(self):
        # Act
        result = Blob.get_all_by_workspace(self.fixture.workspace_1)
        # Assert
        self.assertTrue(
            all(item.user_id == str(self.fixture.workspace_1.owner) for item in result)
        )

    def test_blob_get_all_by_workspace_return_empty_collection_of_blob_from_empty_workspace(
        self,
    ):
        # Act
        result = Blob.get_all_by_workspace(self.fixture.workspace_without_data)
        # Assert
        self.assertTrue(result.count() == 0)


class TestBlobGetAllByListWorkspace(MongoIntegrationBaseTestCase):

    fixture = fixture_blob_workspace

    def test_blob_get_all_by_workspace_return_collection_of_blob_from_user(self):
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
        # Act
        result = Blob.get_all_by_list_workspace([self.fixture.workspace_without_data])
        # Assert
        self.assertTrue(result.count() == 0)
