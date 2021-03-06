""" Authentication tests for Blob REST API
"""
from django.test import SimpleTestCase
from mock import Mock
from mock.mock import patch
from rest_framework import status

import core_main_app.components.blob.api as blob_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.components.blob.models import Blob
from core_main_app.rest.blob import views as blob_rest_views
from core_main_app.rest.blob.serializers import BlobSerializer, DeleteBlobsSerializer
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestBlobListAdminGetPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            blob_rest_views.BlobListAdmin.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            blob_rest_views.BlobListAdmin.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.blob.api.get_all")
    def test_staff_returns_http_200(self, get_all):
        mock_user = create_mock_user("1", is_staff=True)
        response = RequestMock.do_request_get(
            blob_rest_views.BlobListAdmin.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestBlobListGetPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(blob_rest_views.BlobList.as_view(), None)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_200(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            blob_rest_views.BlobList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_returns_http_200(self):
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            blob_rest_views.BlobList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestBlobListPostPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_post(blob_rest_views.BlobList.as_view(), None)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(BlobSerializer, "data")
    @patch.object(BlobSerializer, "save")
    @patch.object(BlobSerializer, "is_valid")
    def test_authenticated_returns_http_201(
        self,
        mock_blob_serializer_is_valid,
        mock_blob_serializer_save,
        mock_blob_serializer_data,
    ):
        mock_blob_serializer_is_valid.return_value = True
        mock_blob_serializer_save.return_value = None
        mock_blob_serializer_data.return_value = []

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            blob_rest_views.BlobList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(BlobSerializer, "data")
    @patch.object(BlobSerializer, "save")
    @patch.object(BlobSerializer, "is_valid")
    def test_staff_returns_http_201(
        self,
        mock_blob_serializer_is_valid,
        mock_blob_serializer_save,
        mock_blob_serializer_data,
    ):
        mock_blob_serializer_is_valid.return_value = True
        mock_blob_serializer_save.return_value = None
        mock_blob_serializer_data.return_value = []

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            blob_rest_views.BlobList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestBlobDetailGetPermissions(SimpleTestCase):
    @patch.object(BlobSerializer, "data")
    @patch.object(blob_api, "get_by_id")
    def test_anonymous_returns_http_200(
        self, mock_blob_api_get_by_id, mock_blob_serializer_data
    ):
        mock_blob_api_get_by_id.return_value = None
        mock_blob_serializer_data.return_value = []

        response = RequestMock.do_request_get(
            blob_rest_views.BlobDetail.as_view(), None, param={"pk": "0"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(BlobSerializer, "data")
    @patch.object(blob_api, "get_by_id")
    def test_authenticated_returns_http_200(
        self, mock_blob_api_get_by_id, mock_blob_serializer_data
    ):
        mock_blob_api_get_by_id.return_value = []
        mock_blob_serializer_data.return_value = []

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            blob_rest_views.BlobDetail.as_view(), mock_user, param={"pk": "0"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(BlobSerializer, "data")
    @patch.object(blob_api, "get_by_id")
    def test_staff_returns_http_200(
        self, mock_blob_api_get_by_id, mock_blob_serializer_data
    ):
        mock_blob_api_get_by_id.return_value = []
        mock_blob_serializer_data.return_value = []

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            blob_rest_views.BlobDetail.as_view(), mock_user, param={"pk": "0"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestBlobDetailDeletePermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_delete(
            blob_rest_views.BlobDetail.as_view(), None, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_api, "delete")
    @patch.object(blob_api, "get_by_id")
    def test_authenticated_returns_http_204(
        self, mock_blob_api_get_by_id, mock_blob_api_delete
    ):
        mock_blob_api_get_by_id.return_value = None
        mock_blob_api_delete.return_value = None

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            blob_rest_views.BlobDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(blob_api, "delete")
    @patch.object(blob_api, "get_by_id")
    def test_staff_returns_http_204(
        self, mock_blob_api_get_by_id, mock_blob_api_delete
    ):
        mock_blob_api_get_by_id.return_value = None
        mock_blob_api_delete.return_value = None

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_delete(
            blob_rest_views.BlobDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestBlobDownloadGetPermissions(SimpleTestCase):
    @patch.object(blob_api, "get_by_id")
    def test_anonymous_returns_http_200(self, mock_blob_api_get_by_id):
        mock_blob = Mock()
        mock_blob.blob = "blob_text"
        mock_blob.filename = "blob.txt"

        mock_blob_api_get_by_id.return_value = mock_blob

        response = RequestMock.do_request_get(
            blob_rest_views.BlobDownload.as_view(), None, param={"pk": "0"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(blob_api, "get_by_id")
    def test_authenticated_returns_http_200(self, mock_blob_api_get_by_id):
        mock_blob = Mock()
        mock_blob.blob = "blob_text"
        mock_blob.filename = "blob.txt"

        mock_blob_api_get_by_id.return_value = mock_blob

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            blob_rest_views.BlobDownload.as_view(), mock_user, param={"pk": "0"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(blob_api, "get_by_id")
    def test_staff_returns_http_200(self, mock_blob_api_get_by_id):
        mock_blob = Mock()
        mock_blob.blob = "blob_text"
        mock_blob.filename = "blob.txt"

        mock_blob_api_get_by_id.return_value = mock_blob

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            blob_rest_views.BlobDownload.as_view(), mock_user, param={"pk": "0"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestBlobDeleteListPatchPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_patch(
            blob_rest_views.BlobDeleteList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(DeleteBlobsSerializer, "validated_data")
    @patch.object(DeleteBlobsSerializer, "is_valid")
    def test_authenticated_returns_http_204(
        self, mock_blob_serializer_is_valid, mock_blob_serializer_validated_data
    ):
        mock_blob_serializer_is_valid.return_value = True
        mock_blob_serializer_validated_data.return_value = list()

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            blob_rest_views.BlobDeleteList.as_view(), mock_user, data=[]
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(DeleteBlobsSerializer, "validated_data")
    @patch.object(DeleteBlobsSerializer, "is_valid")
    def test_staff_returns_http_204(
        self, mock_blob_serializer_is_valid, mock_blob_serializer_validated_data
    ):
        mock_blob_serializer_is_valid.return_value = True
        mock_blob_serializer_validated_data.return_value = list()

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            blob_rest_views.BlobDeleteList.as_view(), mock_user, data=[]
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestBlobAssignPatchPermissions(SimpleTestCase):
    @patch.object(blob_api, "assign")
    @patch.object(workspace_api, "get_by_id")
    @patch.object(blob_api, "get_by_id")
    def test_anonymous_returns_http_403(
        self,
        mock_data_api_get_by_id,
        mock_workspace_api_get_by_id,
        mock_data_api_assign,
    ):
        mock_data_api_get_by_id.return_value = None
        mock_workspace_api_get_by_id.return_value = None
        mock_data_api_assign.return_value = None

        response = RequestMock.do_request_patch(
            blob_rest_views.BlobAssign.as_view(),
            None,
            param={"pk": 0, "workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_api, "assign")
    @patch.object(workspace_api, "get_by_id")
    @patch.object(blob_api, "get_by_id")
    def test_authenticated_returns_http_200(
        self,
        mock_blob_api_get_by_id,
        mock_workspace_api_get_by_id,
        mock_blob_api_assign,
    ):
        mock_blob_api_get_by_id.return_value = None
        mock_workspace_api_get_by_id.return_value = None
        mock_blob_api_assign.return_value = None

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            blob_rest_views.BlobAssign.as_view(),
            mock_user,
            param={"pk": 0, "workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(blob_api, "assign")
    @patch.object(workspace_api, "get_by_id")
    @patch.object(blob_api, "get_by_id")
    def test_staff_returns_http_200(
        self,
        mock_blob_api_get_by_id,
        mock_workspace_api_get_by_id,
        mock_blob_api_assign,
    ):
        mock_blob_api_get_by_id.return_value = None
        mock_workspace_api_get_by_id.return_value = None
        mock_blob_api_assign.return_value = None

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            blob_rest_views.BlobAssign.as_view(),
            mock_user,
            param={"pk": 0, "workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestBlobChangeOwnerPatchPermissions(SimpleTestCase):
    @patch.object(blob_api, "change_owner")
    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Blob, "get_by_id")
    def test_anonymous_returns_http_403(
        self,
        mock_blob_api_get_by_id,
        mock_user_api_get_by_id,
        mock_blob_api_change_owner,
    ):
        mock_blob_api_get_by_id.return_value = None
        mock_user_api_get_by_id.return_value = None
        mock_blob_api_change_owner.return_value = None

        response = RequestMock.do_request_patch(
            blob_rest_views.BlobChangeOwner.as_view(),
            None,
            param={"pk": 0, "user_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_api, "change_owner")
    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Blob, "get_by_id")
    def test_authenticated_returns_http_403(
        self,
        mock_blob_api_get_by_id,
        mock_user_api_get_by_id,
        mock_blob_api_change_owner,
    ):
        mock_blob_api_get_by_id.return_value = None
        mock_user_api_get_by_id.return_value = None
        mock_blob_api_change_owner.return_value = None

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            blob_rest_views.BlobChangeOwner.as_view(),
            mock_user,
            param={"pk": 0, "user_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_api, "change_owner")
    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Blob, "get_by_id")
    def test_staff_returns_http_200(
        self,
        mock_blob_api_get_by_id,
        mock_user_api_get_by_id,
        mock_blob_api_change_owner,
    ):
        # Arrange
        # is_staff to access the view
        # is_superuser to be able to change the owner
        user_request = create_mock_user("1", is_staff=True, is_superuser=True)
        mock_blob_api_get_by_id.return_value = None
        mock_user_api_get_by_id.return_value = None
        mock_blob_api_change_owner.return_value = None

        # Act
        response = RequestMock.do_request_patch(
            blob_rest_views.BlobChangeOwner.as_view(),
            user_request,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
