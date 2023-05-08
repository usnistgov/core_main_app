""" Integration Test for Blob Rest API
"""
from os.path import join, dirname, abspath
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from tests.components.blob.fixtures.fixtures import (
    BlobFixtures,
    AccessControlBlobFixture,
)
from tests.components.data.fixtures.fixtures import (
    AccessControlBlobWithMetadataFixture,
)

from core_main_app.components.blob.models import Blob
from core_main_app.components.workspace.models import Workspace
from core_main_app.rest.blob import views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

RESOURCES_PATH = join(dirname(abspath(__file__)), "data")
fixture_blob = BlobFixtures()
fixture_blob_workspace = AccessControlBlobFixture()
fixture_blob_metadata = AccessControlBlobWithMetadataFixture()


class TestBlobListAdmin(IntegrationBaseTestCase):
    """TestBlobListAdmin"""

    fixture = fixture_blob

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_as_user_returns_http_403(self):
        """test_get_as_user_returns_http_403

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BlobListAdmin.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_as_superuser_returns_all_blobs(self):
        """test_get_as_superuser_returns_all_blobs

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True, is_superuser=True)

        # Act
        response = RequestMock.do_request_get(
            views.BlobListAdmin.as_view(), user
        )

        # Assert
        self.assertEqual(len(response.data), 3)


class TestBlobList(IntegrationBaseTestCase):
    """TestBlobList"""

    fixture = fixture_blob

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        self.data = {
            "blob": SimpleUploadedFile("blob.txt", b"blob"),
        }

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_http_200(self):
        """test_get_returns_http_200

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(), user)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_all_user_blobs(self):
        """test_get_returns_all_user_blobs

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(), user)

        # Assert
        self.assertEqual(len(response.data), 2)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_as_superuser_returns_all_user_blobs(self):
        """test_get_as_superuser_returns_all_user_blobs

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(), user)

        # Assert
        self.assertEqual(len(response.data), 2)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_filtered_by_correct_name_returns_http_200(self):
        """test_get_filtered_by_correct_name_returns_http_200

        Returns:

        """
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
        """test_get_filtered_by_correct_name_returns_correct_blob

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_get(
            views.BlobList.as_view(),
            user,
            data={"filename": self.fixture.blob_1.filename},
        )

        # Assert
        self.assertEqual(
            response.data[0]["filename"], self.fixture.blob_1.filename
        )

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_filtered_by_incorrect_name_returns_http_200(self):
        """test_get_filtered_by_incorrect_name_returns_http_200

        Returns:

        """
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
        """test_get_filtered_by_incorrect_name_returns_empty_list

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_get(
            views.BlobList.as_view(), user, data={"filename": "incorrect"}
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_returns_http_201(self):
        """test_post_returns_http_201

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_post(
            views.BlobList.as_view(), user, data=self.data, content_type=None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["filename"], self.data["blob"].name)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_with_filename_returns_http_201(self):
        """test_post_returns_http_201

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        self.data["filename"] = "test.txt"

        # Act
        response = RequestMock.do_request_post(
            views.BlobList.as_view(), user, data=self.data, content_type=None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["filename"], self.data["filename"])

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_adds_an_entry_in_database(self):
        """test_post_adds_an_entry_in_database

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        number_of_blobs = Blob.get_all().count()

        # Act
        RequestMock.do_request_post(
            views.BlobList.as_view(), user, data=self.data, content_type=None
        )

        # Assert
        self.assertEqual(Blob.get_all().count(), number_of_blobs + 1)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_incorrect_file_parameter_returns_http_400(self):
        """test_post_incorrect_file_parameter_returns_http_400

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        self.data["blob"] = "test.txt"

        # Act
        response = RequestMock.do_request_post(
            views.BlobList.as_view(), user, data=self.data, content_type=None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestBlobDetail(IntegrationBaseTestCase):
    """TestBlobDetail"""

    fixture = fixture_blob

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_http_200(self):
        """test_get_returns_http_200

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDetail.as_view(),
            user,
            param={"pk": str(self.fixture.blob_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_blob(self):
        """test_get_returns_blob

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDetail.as_view(),
            user,
            param={"pk": str(self.fixture.blob_1.id)},
        )

        # Assert
        self.assertEqual(
            response.data["filename"], self.fixture.blob_1.filename
        )

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_wrong_id_returns_http_404(self):
        """test_get_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDetail.as_view(), user, param={"pk": -1}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_other_user_blob_returns_http_403(self):
        """test_get_other_user_blob_returns_http_403

        Returns:

        """
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDetail.as_view(),
            user,
            param={"pk": str(self.fixture.blob_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_returns_http_204(self):
        """test_delete_returns_http_204

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            views.BlobDetail.as_view(),
            user,
            param={"pk": str(self.fixture.blob_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_deletes_one_blob_from_database(self):
        """test_delete_deletes_one_blob_from_database

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        RequestMock.do_request_delete(
            views.BlobDetail.as_view(),
            user,
            param={"pk": str(self.fixture.blob_1.id)},
        )

        # Assert
        self.assertEqual(len(Blob.get_all()), 2)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_wrong_id_returns_http_404(self):
        """test_delete_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            views.BlobDetail.as_view(), user, param={"pk": -1}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_other_user_blob_returns_http_403(self):
        """test_delete_other_user_blob_returns_http_403

        Returns:

        """
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_delete(
            views.BlobDetail.as_view(),
            user,
            param={"pk": str(self.fixture.blob_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_other_user_as_superuser_returns_http_204(self):
        """test_delete_other_user_as_superuser_returns_http_204

        Returns:

        """
        # Arrange
        user = create_mock_user("2", is_superuser=True)

        # Act
        response = RequestMock.do_request_delete(
            views.BlobDetail.as_view(),
            user,
            param={"pk": str(self.fixture.blob_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestBlobDownload(IntegrationBaseTestCase):
    """TestBlobDownload"""

    fixture = fixture_blob

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        self.blob = open(join(RESOURCES_PATH, "test.txt"), "r").read()

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_http_200(self):
        """test_get_returns_http_200

        Returns:

        """
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
        """test_get_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDownload.as_view(), user, param={"pk": -1}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_other_user_blob_returns_http_403(self):
        """test_get_other_user_blob_returns_http_403

        Returns:

        """
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_get(
            views.BlobDownload.as_view(),
            user,
            param={"pk": str(self.fixture.blob_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestBlobDeleteList(IntegrationBaseTestCase):
    """TestBlobDeleteList"""

    fixture = fixture_blob

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        self.data = [
            {"id": str(self.fixture.blob_1.id)},
            {"id": str(self.fixture.blob_2.id)},
        ]

    def test_post_a_list_containing_other_user_blob_returns_http_403(self):
        """test_post_a_list_containing_other_user_blob_returns_http_403

        Returns:

        """
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.BlobDeleteList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_a_list_containing_other_user_blob_as_superuser_returns_http_204(
        self,
    ):
        """test_post_a_list_containing_other_user_blob_as_superuser_returns_http_204

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            views.BlobDeleteList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestBlobAssign(IntegrationBaseTestCase):
    """TestBlobAssign"""

    fixture = fixture_blob_workspace

    @patch.object(Workspace, "get_by_id")
    @patch.object(Blob, "get_by_id")
    def test_get_returns_http_200(self, blob_get_by_id, workspace_get_by_id):
        """test_get_returns_http_200

        Args:
            blob_get_by_id:
            workspace_get_by_id:

        Returns:

        """
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
        """test_assign_blob_to_workspace_updates_workspace

        Args:
            blob_get_by_id:
            workspace_get_by_id:

        Returns:

        """
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
        self.assertEqual(
            str(blob.workspace.id), str(self.fixture.workspace_2.id)
        )

    @patch.object(Workspace, "get_by_id")
    @patch.object(Blob, "get_by_id")
    def test_assign_blob_to_workspace_returns_http_200(
        self, blob_get_by_id, workspace_get_by_id
    ):
        """test_assign_blob_to_workspace_returns_http_200

        Args:
            blob_get_by_id:
            workspace_get_by_id:

        Returns:

        """
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
        """test_assign_bad_blob_id_returns_http_404

        Args:
            workspace_get_by_id:

        Returns:

        """
        # Arrange
        fake_blob_id = -1
        user = create_mock_user("1", is_superuser=True)
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        response = RequestMock.do_request_patch(
            views.BlobAssign.as_view(),
            user,
            param={
                "pk": fake_blob_id,
                "workspace_id": self.fixture.workspace_2.id,
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(Blob, "get_by_id")
    def test_assign_bad_workspace_id_returns_http_404(self, blob_get_by_id):
        """test_assign_bad_workspace_id_returns_http_404

        Args:
            blob_get_by_id:

        Returns:

        """
        # Arrange
        fake_workspace_id = -1
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


class TestBlobChangeOwner(IntegrationBaseTestCase):
    """TestBlobChangeOwner"""

    fixture = fixture_blob_workspace

    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Blob, "get_by_id")
    def test_get_returns_http_200_if_user_is_superuser(
        self, blob_get_by_id, user_get_by_id
    ):
        """test_get_returns_http_200_if_user_is_superuser

        Args:
            blob_get_by_id:
            user_get_by_id:

        Returns:

        """
        # Arrange
        blob = self.fixture.blob_collection[self.fixture.USER_1_WORKSPACE_1]
        user_request = create_mock_user(
            "65467", is_staff=True, is_superuser=True
        )
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
        """test_get_returns_http_200_if_user_is_not_superuser_but_have_access_to_the_blob

        Args:
            blob_get_by_id:
            user_get_by_id:

        Returns:

        """
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
        """test_get_returns_http_403_if_user_is_not_superuser_or_have_no_access_to_the_blob

        Args:
            blob_get_by_id:
            user_get_by_id:
            read_access_mock:

        Returns:

        """
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


class TestBlobAddMetadata(IntegrationBaseTestCase):
    """TestBlobAddMetadata"""

    fixture = fixture_blob_metadata

    def test_add_metadata_authorized_returns_http_200(
        self,
    ):
        """test_add_metadata_authorized_returns_http_200

        Args:

        Returns:

        """
        # Arrange
        blob = self.fixture.blob_1
        mock_user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_post(
            views.BlobMetadata.as_view(),
            mock_user,
            param={"pk": blob.id, "metadata_id": self.fixture.data_4.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core_main_app.components.blob.api.add_metadata")
    def test_add_metadata_with_errors_returns_http_500(self, add_metadata):
        """test_add_metadata_with_errors_returns_http_500

        Args:

        Returns:

        """
        # Arrange
        blob = self.fixture.blob_1
        mock_user = create_mock_user("1")
        add_metadata.side_effect = Exception()

        # Act
        response = RequestMock.do_request_post(
            views.BlobMetadata.as_view(),
            mock_user,
            param={"pk": blob.id, "metadata_id": self.fixture.data_4.id},
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_add_metadata_unauthorized_returns_http_403(
        self,
        get_all_workspaces_with_read_access_by_user,
        get_all_workspaces_with_write_access_by_user,
    ):
        """test_add_metadata_unauthorized_returns_http_403

        Args:

        Returns:

        """
        # Arrange
        blob = self.fixture.blob_3
        mock_user = create_mock_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        get_all_workspaces_with_write_access_by_user.return_value = []

        # Act
        response = RequestMock.do_request_post(
            views.BlobMetadata.as_view(),
            mock_user,
            param={"pk": blob.id, "metadata_id": self.fixture.data_4.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_metadata_wrong_blob_id_returns_http_404(
        self,
    ):
        """test_add_metadata_wrong_blob_id_returns_http_404

        Args:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_post(
            views.BlobMetadata.as_view(),
            mock_user,
            param={"pk": "1234", "metadata_id": self.fixture.data_4.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_metadata_wrong_data_id_returns_http_404(
        self,
    ):
        """test_add_metadata_wrong_data_id_returns_http_404

        Args:

        Returns:

        """
        # Arrange
        blob = self.fixture.blob_1
        mock_user = create_mock_user("1")
        # Act
        response = RequestMock.do_request_post(
            views.BlobMetadata.as_view(),
            mock_user,
            param={"pk": blob.id, "metadata_id": "1234"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestBlobRemoveMetadata(IntegrationBaseTestCase):
    """TestBlobRemoveMetadata"""

    fixture = fixture_blob_metadata

    def test_remove_metadata_authorized_returns_http_200(
        self,
    ):
        """test_remove_metadata_authorized_returns_http_200

        Args:

        Returns:

        """
        # Arrange
        blob = self.fixture.blob_1
        mock_user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            views.BlobMetadata.as_view(),
            mock_user,
            param={"pk": blob.id, "metadata_id": self.fixture.data_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core_main_app.components.blob.api.remove_metadata")
    def test_remove_metadata_with_errors_returns_http_500(
        self, remove_metadata
    ):
        """test_remove_metadata_with_errors_returns_http_500

        Args:

        Returns:

        """
        # Arrange
        blob = self.fixture.blob_1
        mock_user = create_mock_user("1")
        remove_metadata.side_effect = Exception()

        # Act
        response = RequestMock.do_request_delete(
            views.BlobMetadata.as_view(),
            mock_user,
            param={"pk": blob.id, "metadata_id": self.fixture.data_1.id},
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_remove_metadata_unauthorized_returns_http_403(
        self,
        get_all_workspaces_with_read_access_by_user,
        get_all_workspaces_with_write_access_by_user,
    ):
        """test_remove_metadata_unauthorized_returns_http_403

        Args:

        Returns:

        """
        # Arrange
        blob = self.fixture.blob_3
        mock_user = create_mock_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = []
        get_all_workspaces_with_write_access_by_user.return_value = []

        # Act
        response = RequestMock.do_request_delete(
            views.BlobMetadata.as_view(),
            mock_user,
            param={"pk": blob.id, "metadata_id": self.fixture.data_32.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_metadata_wrong_blob_id_returns_http_404(
        self,
    ):
        """test_remove_metadata_wrong_blob_id_returns_http_404

        Args:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            views.BlobMetadata.as_view(),
            mock_user,
            param={"pk": "1234", "metadata_id": self.fixture.data_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_metadata_wrong_data_id_returns_http_404(
        self,
    ):
        """test_remove_metadata_wrong_data_id_returns_http_404

        Args:

        Returns:

        """
        # Arrange
        blob = self.fixture.blob_1
        mock_user = create_mock_user("1")
        # Act
        response = RequestMock.do_request_delete(
            views.BlobMetadata.as_view(),
            mock_user,
            param={"pk": blob.id, "metadata_id": "1234"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
