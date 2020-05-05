""" Integration Test for Blob Rest API
"""
import unittest
from os.path import join, dirname, abspath

from django.test import override_settings
from mock import patch
from rest_framework import status

from core_main_app.components.blob import api as blob_api
from core_main_app.components.blob.models import Blob
from core_main_app.components.workspace.models import Workspace
from core_main_app.rest.blob import views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests.components.blob.fixtures.fixtures import (
    BlobFixtures,
    AccessControlBlobFixture,
)

RESOURCES_PATH = join(dirname(abspath(__file__)), "data")
fixture_blob = BlobFixtures()
fixture_blob_workspace = AccessControlBlobFixture()


class TestBlobListAdmin(MongoIntegrationBaseTestCase):
    fixture = fixture_blob

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_as_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(views.BlobListAdmin.as_view(), user)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_as_superuser_returns_all_blobs(self):
        # Arrange
        user = create_mock_user("1", is_staff=True, is_superuser=True)

        # Act
        response = RequestMock.do_request_get(views.BlobListAdmin.as_view(), user)

        # Assert
        self.assertEqual(len(response.data), 3)


class TestBlobList(MongoIntegrationBaseTestCase):
    fixture = fixture_blob

    def setUp(self):
        super(TestBlobList, self).setUp()
        self.data = {
            "filename": "file.txt",
            "blob": open(join(RESOURCES_PATH, "test.txt"), "r"),
        }

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_http_200(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(), user)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_all_user_blobs(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(), user)

        # Assert
        self.assertEqual(len(response.data), 2)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_as_superuser_returns_all_user_blobs(self):
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(), user)

        # Assert
        self.assertEqual(len(response.data), 2)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_filtered_by_correct_name_returns_http_200(self):
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_get(
            views.BlobList.as_view(),
            user,
            data={"filename": self.fixture.blob_1.filename},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_filtered_by_correct_name_returns_correct_blob(self):
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_get(
            views.BlobList.as_view(),
            user,
            data={"filename": self.fixture.blob_1.filename},
        )

        # Assert
        self.assertEqual(response.data[0]["filename"], self.fixture.blob_1.filename)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_filtered_by_incorrect_name_returns_http_200(self):
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_get(
            views.BlobList.as_view(), user, data={"filename": "incorrect"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_filtered_by_incorrect_name_returns_empty_list(self):
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_get(
            views.BlobList.as_view(), user, data={"filename": "incorrect"}
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_returns_http_201(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_post(
            views.BlobList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_adds_an_entry_in_database(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_post(
            views.BlobList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(len(blob_api.get_all()), 4)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_incorrect_file_parameter_returns_http_400(self):
        # Arrange
        user = create_mock_user("1")
        self.data["blob"] = "test.txt"

        # Act
        response = RequestMock.do_request_post(
            views.BlobList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestBlobDetail(MongoIntegrationBaseTestCase):
    fixture = fixture_blob

    def setUp(self):
        super(TestBlobDetail, self).setUp()

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_http_200(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDetail.as_view(), user, param={"pk": str(self.fixture.blob_1.id)}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_blob(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDetail.as_view(), user, param={"pk": str(self.fixture.blob_1.id)}
        )

        # Assert
        self.assertEqual(response.data["filename"], self.fixture.blob_1.filename)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDetail.as_view(), user, param={"pk": "507f1f77bcf86cd799439011"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_other_user_blob_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDetail.as_view(), user, param={"pk": str(self.fixture.blob_1.id)}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_returns_http_204(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            views.BlobDetail.as_view(), user, param={"pk": str(self.fixture.blob_1.id)}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_deletes_one_blob_from_database(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            views.BlobDetail.as_view(), user, param={"pk": str(self.fixture.blob_1.id)}
        )

        # Assert
        self.assertEqual(len(blob_api.get_all()), 2)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            views.BlobDetail.as_view(), user, param={"pk": "507f1f77bcf86cd799439011"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_other_user_blob_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_delete(
            views.BlobDetail.as_view(), user, param={"pk": str(self.fixture.blob_1.id)}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_other_user_as_superuser_returns_http_204(self):
        # Arrange
        user = create_mock_user("2", is_superuser=True)

        # Act
        response = RequestMock.do_request_delete(
            views.BlobDetail.as_view(), user, param={"pk": str(self.fixture.blob_1.id)}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestBlobDownload(MongoIntegrationBaseTestCase):
    fixture = fixture_blob

    def setUp(self):
        super(TestBlobDownload, self).setUp()
        self.blob = open(join(RESOURCES_PATH, "test.txt"), "r").read()

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_http_200(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDownload.as_view(),
            user,
            param={"pk": str(self.fixture.blob_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDownload.as_view(), user, param={"pk": "507f1f77bcf86cd799439011"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_other_user_blob_returns_http_200(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDownload.as_view(),
            user,
            param={"pk": str(self.fixture.blob_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestBlobDeleteList(MongoIntegrationBaseTestCase):
    fixture = fixture_blob

    def setUp(self):
        super(TestBlobDeleteList, self).setUp()
        self.data = [
            {"id": str(self.fixture.blob_1.id)},
            {"id": str(self.fixture.blob_2.id)},
        ]

    def test_post_a_list_containing_other_user_blob_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.BlobDeleteList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @unittest.skip("need to mock GridFS Blob Host")
    def test_post_a_list_containing_other_user_blob_as_superuser_returns_http_204(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            views.BlobDeleteList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestBlobAssign(MongoIntegrationBaseTestCase):
    fixture = fixture_blob_workspace

    @patch.object(Workspace, "get_by_id")
    @patch.object(Blob, "get_by_id")
    def test_get_returns_http_200(self, blob_get_by_id, workspace_get_by_id):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob
        workspace_get_by_id.return_value = self.fixture.workspace_1

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Workspace, "get_by_id")
    @patch.object(Blob, "get_by_id")
    def test_assign_blob_to_workspace_updates_workspace(
        self, blob_get_by_id, workspace_get_by_id
    ):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": self.fixture.workspace_2.id},
        )

        # Assert
        self.assertEqual(str(blob.workspace.id), str(self.fixture.workspace_2.id))

    @patch.object(Workspace, "get_by_id")
    @patch.object(Blob, "get_by_id")
    def test_assign_blob_to_workspace_returns_http_200(
        self, blob_get_by_id, workspace_get_by_id
    ):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": self.fixture.workspace_2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Workspace, "get_by_id")
    def test_assign_bad_blob_id_returns_http_404(self, workspace_get_by_id):
        # Arrange
        fake_blob_id = "507f1f77bcf86cd799439011"
        user = create_mock_user("1", is_superuser=True)
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": fake_blob_id, "workspace_id": self.fixture.workspace_2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(Blob, "get_by_id")
    def test_assign_bad_workspace_id_returns_http_404(self, blob_get_by_id):
        # Arrange
        fake_workspace_id = "507f1f77bcf86cd799439011"
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": fake_workspace_id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestBlobAssign(MongoIntegrationBaseTestCase):
    fixture = fixture_blob_workspace

    @patch.object(Workspace, "get_by_id")
    @patch.object(Blob, "get_by_id")
    def test_get_returns_http_200(self, blob_get_by_id, workspace_get_by_id):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob
        workspace_get_by_id.return_value = self.fixture.workspace_1

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Workspace, "get_by_id")
    @patch.object(Blob, "get_by_id")
    def test_assign_blob_to_workspace_updates_workspace(
        self, blob_get_by_id, workspace_get_by_id
    ):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": self.fixture.workspace_2.id},
        )

        # Assert
        self.assertEqual(str(blob.workspace.id), str(self.fixture.workspace_2.id))

    @patch.object(Workspace, "get_by_id")
    @patch.object(Blob, "get_by_id")
    def test_assign_blob_to_workspace_returns_http_200(
        self, blob_get_by_id, workspace_get_by_id
    ):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": self.fixture.workspace_2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Workspace, "get_by_id")
    def test_assign_bad_blob_id_returns_http_404(self, workspace_get_by_id):
        # Arrange
        fake_blob_id = "507f1f77bcf86cd799439011"
        user = create_mock_user("1", is_superuser=True)
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": fake_blob_id, "workspace_id": self.fixture.workspace_2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(Blob, "get_by_id")
    def test_assign_bad_workspace_id_returns_http_404(self, blob_get_by_id):
        # Arrange
        fake_workspace_id = "507f1f77bcf86cd799439011"
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": fake_workspace_id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestBlobAssign(MongoIntegrationBaseTestCase):
    fixture = fixture_blob_workspace

    @patch.object(Workspace, "get_by_id")
    @patch.object(Blob, "get_by_id")
    def test_get_returns_http_200(self, blob_get_by_id, workspace_get_by_id):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob
        workspace_get_by_id.return_value = self.fixture.workspace_1

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Workspace, "get_by_id")
    @patch.object(Blob, "get_by_id")
    def test_assign_blob_to_workspace_updates_workspace(
        self, blob_get_by_id, workspace_get_by_id
    ):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": self.fixture.workspace_2.id},
        )

        # Assert
        self.assertEqual(str(blob.workspace.id), str(self.fixture.workspace_2.id))

    @patch.object(Workspace, "get_by_id")
    @patch.object(Blob, "get_by_id")
    def test_assign_blob_to_workspace_returns_http_200(
        self, blob_get_by_id, workspace_get_by_id
    ):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": self.fixture.workspace_2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Workspace, "get_by_id")
    def test_assign_bad_blob_id_returns_http_404(self, workspace_get_by_id):
        # Arrange
        fake_blob_id = "507f1f77bcf86cd799439011"
        user = create_mock_user("1", is_superuser=True)
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": fake_blob_id, "workspace_id": self.fixture.workspace_2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(Blob, "get_by_id")
    def test_assign_bad_workspace_id_returns_http_404(self, blob_get_by_id):
        # Arrange
        fake_workspace_id = "507f1f77bcf86cd799439011"
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(blob.user_id, is_superuser=True)
        blob_get_by_id.return_value = blob

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={"pk": blob.id, "workspace_id": fake_workspace_id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestBlobChangeOwner(MongoIntegrationBaseTestCase):
    fixture = fixture_blob_workspace

    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Blob, "get_by_id")
    def test_get_returns_http_200_if_user_is_superuser(
        self, blob_get_by_id, user_get_by_id
    ):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user_request = create_mock_user("65467", is_staff=True, is_superuser=True)
        user_new_owner = create_mock_user("123")
        blob_get_by_id.return_value = blob
        user_get_by_id.return_value = user_new_owner

        # Act
        response = RequestMock.do_request_patch(
            views.BlobChangeOwner.as_view(),
            user_request,
            param={"pk": blob.id, "user_id": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Blob, "get_by_id")
    def test_get_returns_http_200_if_user_is_not_superuser_but_have_access_to_the_blob(
        self, blob_get_by_id, user_get_by_id
    ):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user_request = create_mock_user("1", is_staff=True)
        user_new_owner = create_mock_user("123")
        blob_get_by_id.return_value = blob
        user_get_by_id.return_value = user_new_owner

        # Act
        response = RequestMock.do_request_patch(
            views.BlobChangeOwner.as_view(),
            user_request,
            param={"pk": blob.id, "user_id": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Blob, "get_by_id")
    def test_get_returns_http_403_if_user_is_not_superuser_or_have_no_access_to_the_blob(
        self, blob_get_by_id, user_get_by_id, read_access_mock
    ):
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user_request = create_mock_user("65467", is_staff=True)
        user_new_owner = create_mock_user("123")
        blob_get_by_id.return_value = blob
        user_get_by_id.return_value = user_new_owner
        read_access_mock.return_value = []

        # Act
        response = RequestMock.do_request_patch(
            views.BlobChangeOwner.as_view(),
            user_request,
            param={"pk": blob.id, "user_id": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
