""" Authentication tests for Data REST API
"""
from unittest.mock import patch, Mock

from django.test import SimpleTestCase
from rest_framework import status
from tests.mocks import MockQuerySet

from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.workspace import api as workspace_api
from core_main_app.rest.data import views as data_rest_views
from core_main_app.rest.data.admin_serializers import AdminDataSerializer
from core_main_app.rest.data.serializers import (
    DataSerializer,
)
from core_main_app.rest.data.views import Migration as data_migration
from core_main_app.rest.data.views import Validation as data_validation
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestDataListPostPermissions(SimpleTestCase):
    """TestDataListPostPermissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_post(
            data_rest_views.DataList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(DataSerializer, "is_valid")
    @patch.object(DataSerializer, "save")
    @patch.object(DataSerializer, "data")
    def test_authenticated_returns_http_201(
        self, data_serializer_data, data_serializer_save, data_serializer_valid
    ):
        """test_authenticated_returns_http_201

        Args:
            data_serializer_data:
            data_serializer_save:
            data_serializer_valid:

        Returns:

        """
        data_serializer_valid.return_value = True
        data_serializer_save.return_value = None
        data_serializer_data.return_value = {}

        mock_user = create_mock_user(1)

        response = RequestMock.do_request_post(
            data_rest_views.DataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(DataSerializer, "is_valid")
    @patch.object(DataSerializer, "save")
    @patch.object(DataSerializer, "data")
    def test_staff_returns_http_201(
        self, data_serializer_data, data_serializer_save, data_serializer_valid
    ):
        """test_staff_returns_http_201

        Args:
            data_serializer_data:
            data_serializer_save:
            data_serializer_valid:

        Returns:

        """
        data_serializer_valid.return_value = True
        data_serializer_save.return_value = None
        data_serializer_data.return_value = {}

        mock_user = create_mock_user(1, is_staff=True)

        response = RequestMock.do_request_post(
            data_rest_views.DataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestDataListGetPermissions(SimpleTestCase):
    """TestDataListGetPermissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(Data, "get_all_by_user_id")
    def test_authenticated_returns_http_200(self, data_get_all_by_user):
        """test_authenticated_returns_http_200

        Args:
            data_get_all_by_user:

        Returns:

        """
        data_get_all_by_user.return_value = MockQuerySet()

        mock_user = create_mock_user(1)

        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Data, "get_all_by_user_id")
    def test_staff_returns_http_200(self, data_get_all_by_user):
        """test_staff_returns_http_200

        Args:
            data_get_all_by_user:

        Returns:

        """
        data_get_all_by_user.return_value = MockQuerySet()

        mock_user = create_mock_user(1, is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAdminDataListPostPermissions(SimpleTestCase):
    """TestAdminDataListPostPermissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_post(
            data_rest_views.AdminDataList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user(1)
        response = RequestMock.do_request_post(
            data_rest_views.AdminDataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_http_403(self):
        """test_staff_returns_http_403

        Returns:

        """
        mock_user = create_mock_user(1, is_staff=True)
        response = RequestMock.do_request_post(
            data_rest_views.AdminDataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(AdminDataSerializer, "is_valid")
    @patch.object(AdminDataSerializer, "save")
    @patch.object(AdminDataSerializer, "data")
    def test_superuser_returns_http_201(
        self, data_serializer_data, data_serializer_save, data_serializer_valid
    ):
        """test_superuser_returns_http_201

        Args:
            data_serializer_data:
            data_serializer_save:
            data_serializer_valid:

        Returns:

        """
        data_serializer_valid.return_value = True
        data_serializer_save.return_value = None
        data_serializer_data.return_value = {}

        mock_user = create_mock_user(1, is_staff=True, is_superuser=True)

        response = RequestMock.do_request_post(
            data_rest_views.AdminDataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestAdminDataListGetPermissions(SimpleTestCase):
    """TestAdminDataListGetPermissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            data_rest_views.AdminDataList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user(1)
        response = RequestMock.do_request_get(
            data_rest_views.AdminDataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_http_403(self):
        """test_staff_returns_http_403

        Returns:

        """
        mock_user = create_mock_user(1, is_staff=True)
        response = RequestMock.do_request_get(
            data_rest_views.AdminDataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(Data, "get_all")
    def test_superuser_returns_http_200(self, data_get_all_by_user):
        """test_superuser_returns_http_200

        Args:
            data_get_all_by_user:

        Returns:

        """
        data_get_all_by_user.return_value = {}

        mock_user = create_mock_user(1, is_staff=True, is_superuser=True)

        response = RequestMock.do_request_get(
            data_rest_views.AdminDataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataListByWorkspaceGetPermissions(SimpleTestCase):
    """TestDataListByWorkspaceGetPermissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            data_rest_views.DataListByWorkspace.as_view(),
            None,
            param={"workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_api, "get_all_by_workspace")
    def test_authenticated_returns_http_200(self, data_get_all_by_workspace):
        """test_authenticated_returns_http_200

        Args:
            data_get_all_by_workspace:

        Returns:

        """
        data_get_all_by_workspace.return_value = {}

        mock_user = create_mock_user(1)

        response = RequestMock.do_request_get(
            data_rest_views.DataListByWorkspace.as_view(),
            mock_user,
            param={"workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_all_by_workspace")
    def test_staff_returns_http_200(self, data_get_all_by_workspace):
        """test_staff_returns_http_200

        Args:
            data_get_all_by_workspace:

        Returns:

        """
        data_get_all_by_workspace.return_value = {}

        mock_user = create_mock_user(1, is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.DataListByWorkspace.as_view(),
            mock_user,
            param={"workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataDetailGetPermissions(SimpleTestCase):
    """TestDataDetailGetPermissions"""

    @patch.object(DataSerializer, "data")
    @patch.object(data_api, "get_by_id")
    def test_anonymous_returns_http_200(
        self, mock_data_api_get_by_id, mock_data_serializer_data
    ):
        """test_anonymous_returns_http_200

        Args:
            mock_data_api_get_by_id:
            mock_data_serializer_data:

        Returns:

        """
        mock_data_api_get_by_id.return_value = None
        mock_data_serializer_data.return_value = []

        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(), None, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(DataSerializer, "data")
    @patch.object(data_api, "get_by_id")
    def test_authenticated_returns_http_200(
        self, mock_data_api_get_by_id, mock_data_serializer_data
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_data_api_get_by_id:
            mock_data_serializer_data:

        Returns:

        """
        mock_data_api_get_by_id.return_value = None
        mock_data_serializer_data.return_value = []

        mock_user = create_mock_user(1)
        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(DataSerializer, "data")
    @patch.object(data_api, "get_by_id")
    def test_staff_returns_http_200(
        self, mock_data_api_get_by_id, mock_data_serializer_data
    ):
        """test_staff_returns_http_200

        Args:
            mock_data_api_get_by_id:
            mock_data_serializer_data:

        Returns:

        """
        mock_data_api_get_by_id.return_value = None
        mock_data_serializer_data.return_value = []

        mock_user = create_mock_user(1, is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataDetailDeletePermissions(SimpleTestCase):
    """TestDataDetailDeletePermissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_delete(
            data_rest_views.DataDetail.as_view(), None, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_api, "delete")
    @patch.object(data_api, "get_by_id")
    def test_authenticated_returns_http_204(
        self, mock_data_api_get_by_id, mock_data_api_delete
    ):
        """test_authenticated_returns_http_204

        Args:
            mock_data_api_get_by_id:
            mock_data_api_delete:

        Returns:

        """
        mock_data_api_get_by_id.return_value = None
        mock_data_api_delete.return_value = None

        mock_user = create_mock_user(1)

        response = RequestMock.do_request_delete(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(data_api, "delete")
    @patch.object(data_api, "get_by_id")
    def test_staff_returns_http_204(
        self, mock_data_api_get_by_id, mock_data_api_delete
    ):
        """test_staff_returns_http_204

        Args:
            mock_data_api_get_by_id:
            mock_data_api_delete:

        Returns:

        """
        mock_data_api_get_by_id.return_value = None
        mock_data_api_delete.return_value = None

        mock_user = create_mock_user(1, is_staff=True)

        response = RequestMock.do_request_delete(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestDataDetailPatchPermissions(SimpleTestCase):
    """TestDataDetailPatchPermissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_patch(
            data_rest_views.DataDetail.as_view(), None, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(DataSerializer, "data")
    @patch.object(DataSerializer, "save")
    @patch.object(DataSerializer, "is_valid")
    @patch.object(data_api, "get_by_id")
    def test_authenticated_returns_http_200(
        self,
        mock_data_api_get_by_id,
        mock_data_serializer_is_valid,
        mock_data_serializer_save,
        mock_data_serializer_data,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_data_api_get_by_id:
            mock_data_serializer_is_valid:
            mock_data_serializer_save:
            mock_data_serializer_data:

        Returns:

        """
        mock_data_api_get_by_id.return_value = []
        mock_data_serializer_is_valid.return_value = True
        mock_data_serializer_save.return_valie = None
        mock_data_serializer_data.return_value = []

        mock_user = create_mock_user(1)

        response = RequestMock.do_request_patch(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(DataSerializer, "data")
    @patch.object(DataSerializer, "save")
    @patch.object(DataSerializer, "is_valid")
    @patch.object(data_api, "get_by_id")
    def test_staff_returns_http_200(
        self,
        mock_data_api_get_by_id,
        mock_data_serializer_is_valid,
        mock_data_serializer_save,
        mock_data_serializer_data,
    ):
        """test_staff_returns_http_200

        Args:
            mock_data_api_get_by_id:
            mock_data_serializer_is_valid:
            mock_data_serializer_save:
            mock_data_serializer_data:

        Returns:

        """
        mock_data_api_get_by_id.return_value = []
        mock_data_serializer_is_valid.return_value = True
        mock_data_serializer_save.return_valie = None
        mock_data_serializer_data.return_value = []

        mock_user = create_mock_user(1, is_staff=True)

        response = RequestMock.do_request_patch(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataDownloadGetPermissions(SimpleTestCase):
    """TestDataDownloadGetPermissions"""

    @patch.object(data_api, "get_by_id")
    def test_anonymous_returns_http_200(self, mock_data_api_get_by_id):
        """test_anonymous_returns_http_200

        Args:
            mock_data_api_get_by_id:

        Returns:

        """
        data_object = Mock()
        data_object.content = "<tag attr='attr_val'>tag_val</tag>"
        data_object.title = "mock.xml"

        mock_data_api_get_by_id.return_value = data_object

        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(), None, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_by_id")
    def test_authenticated_returns_http_200(self, mock_data_api_get_by_id):
        """test_authenticated_returns_http_200

        Args:
            mock_data_api_get_by_id:

        Returns:

        """
        data_object = Mock()
        data_object.content = "<tag attr='attr_val'>tag_val</tag>"
        data_object.title = "mock.xml"

        mock_data_api_get_by_id.return_value = data_object

        mock_user = create_mock_user(1)

        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_by_id")
    def test_staff_returns_http_200(self, mock_data_api_get_by_id):
        """test_staff_returns_http_200

        Args:
            mock_data_api_get_by_id:

        Returns:

        """
        data_object = Mock()
        data_object.content = "<tag attr='attr_val'>tag_val</tag>"
        data_object.title = "mock.xml"

        mock_data_api_get_by_id.return_value = data_object

        mock_user = create_mock_user(1, is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataLocalQueryPostPermissions(SimpleTestCase):
    """TestDataLocalQueryPostPermissions"""

    @patch.object(data_api, "execute_query")
    def test_anonymous_returns_http_200(self, mock_data_api_execute_query):
        """test_anonymous_returns_http_200

        Args:
            mock_data_api_execute_query:

        Returns:

        """
        mock_data_api_execute_query.return_value = []

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            None,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "execute_query")
    def test_authenticated_returns_http_200(self, mock_data_api_execute_query):
        """test_authenticated_returns_http_200

        Args:
            mock_data_api_execute_query:

        Returns:

        """
        mock_data_api_execute_query.return_value = []

        mock_user = create_mock_user(1)

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "execute_query")
    def test_staff_returns_http_200(self, mock_data_api_execute_query):
        """test_staff_returns_http_200

        Args:
            mock_data_api_execute_query:

        Returns:

        """
        mock_data_api_execute_query.return_value = []

        mock_user = create_mock_user(1, is_staff=True)

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataKeywordQueryPostPermissions(SimpleTestCase):
    """TestDataKeywordQueryPostPermissions"""

    @patch.object(data_api, "execute_query")
    def test_anonymous_returns_http_200(self, mock_data_api_execute_query):
        """test_anonymous_returns_http_200

        Args:
            mock_data_api_execute_query:

        Returns:

        """
        mock_data_api_execute_query.return_value = []

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalKeywordQueryView.as_view(),
            None,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "execute_query")
    def test_authenticated_returns_http_200(self, mock_data_api_execute_query):
        """test_authenticated_returns_http_200

        Args:
            mock_data_api_execute_query:

        Returns:

        """
        mock_data_api_execute_query.return_value = []

        mock_user = create_mock_user(1)

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalKeywordQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "execute_query")
    def test_staff_returns_http_200(self, mock_data_api_execute_query):
        """test_staff_returns_http_200

        Args:
            mock_data_api_execute_query:

        Returns:

        """
        mock_data_api_execute_query.return_value = []

        mock_user = create_mock_user(1, is_staff=True)

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalKeywordQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataAssignPatchPermissions(SimpleTestCase):
    """TestDataAssignPatchPermissions"""

    @patch.object(data_api, "assign")
    @patch.object(workspace_api, "get_by_id")
    @patch.object(data_api, "get_by_id")
    def test_anonymous_returns_http_403(
        self,
        mock_data_api_get_by_id,
        mock_workspace_api_get_by_id,
        mock_data_api_assign,
    ):
        """test_anonymous_returns_http_403

        Args:
            mock_data_api_get_by_id:
            mock_workspace_api_get_by_id:
            mock_data_api_assign:

        Returns:

        """
        mock_data_api_get_by_id.return_value = None
        mock_workspace_api_get_by_id.return_value = None
        mock_data_api_assign.return_value = None

        response = RequestMock.do_request_patch(
            data_rest_views.DataAssign.as_view(),
            None,
            param={"pk": 0, "workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_api, "assign")
    @patch.object(workspace_api, "get_by_id")
    @patch.object(data_api, "get_by_id")
    def test_authenticated_returns_http_200(
        self,
        mock_data_api_get_by_id,
        mock_workspace_api_get_by_id,
        mock_data_api_assign,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_data_api_get_by_id:
            mock_workspace_api_get_by_id:
            mock_data_api_assign:

        Returns:

        """
        mock_data_api_get_by_id.return_value = None
        mock_workspace_api_get_by_id.return_value = None
        mock_data_api_assign.return_value = None

        mock_user = create_mock_user(1)

        response = RequestMock.do_request_patch(
            data_rest_views.DataAssign.as_view(),
            mock_user,
            param={"pk": 0, "workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "assign")
    @patch.object(workspace_api, "get_by_id")
    @patch.object(data_api, "get_by_id")
    def test_staff_returns_http_200(
        self,
        mock_data_api_get_by_id,
        mock_workspace_api_get_by_id,
        mock_data_api_assign,
    ):
        """test_staff_returns_http_200

        Args:
            mock_data_api_get_by_id:
            mock_workspace_api_get_by_id:
            mock_data_api_assign:

        Returns:

        """
        mock_data_api_get_by_id.return_value = None
        mock_workspace_api_get_by_id.return_value = None
        mock_data_api_assign.return_value = None

        mock_user = create_mock_user(1, is_staff=True)

        response = RequestMock.do_request_patch(
            data_rest_views.DataAssign.as_view(),
            mock_user,
            param={"pk": 0, "workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataChangeOwnerPatchPermissions(SimpleTestCase):
    """TestDataChangeOwnerPatchPermissions"""

    @patch.object(data_api, "change_owner")
    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Data, "get_by_id")
    def test_anonymous_returns_http_403(
        self,
        mock_data_api_get_by_id,
        mock_user_api_get_by_id,
        mock_data_api_change_owner,
    ):
        """test_anonymous_returns_http_403

        Args:
            mock_data_api_get_by_id:
            mock_user_api_get_by_id:
            mock_data_api_change_owner:

        Returns:

        """
        mock_data_api_get_by_id.return_value = None
        mock_user_api_get_by_id.return_value = None
        mock_data_api_change_owner.return_value = None

        response = RequestMock.do_request_patch(
            data_rest_views.DataChangeOwner.as_view(),
            None,
            param={"pk": 0, "user_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_api, "change_owner")
    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Data, "get_by_id")
    def test_authenticated_returns_http_403(
        self,
        mock_data_api_get_by_id,
        mock_user_api_get_by_id,
        mock_data_api_change_owner,
    ):
        """test_authenticated_returns_http_403

        Args:
            mock_data_api_get_by_id:
            mock_user_api_get_by_id:
            mock_data_api_change_owner:

        Returns:

        """
        mock_data_api_get_by_id.return_value = None
        mock_user_api_get_by_id.return_value = None
        mock_data_api_change_owner.return_value = None

        mock_user = create_mock_user(1)

        response = RequestMock.do_request_patch(
            data_rest_views.DataChangeOwner.as_view(),
            mock_user,
            param={"pk": 0, "user_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_api, "change_owner")
    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Data, "get_by_id")
    def test_staff_returns_http_200(
        self,
        mock_data_api_get_by_id,
        mock_user_api_get_by_id,
        mock_data_api_change_owner,
    ):
        """test_staff_returns_http_200

        Args:
            mock_data_api_get_by_id:
            mock_user_api_get_by_id:
            mock_data_api_change_owner:

        Returns:

        """
        # Arrange
        # is_staff to access the view
        # is_superuser to be able to change the owner
        user_request = create_mock_user(1, is_staff=True, is_superuser=True)
        mock_data_api_get_by_id.return_value = None
        mock_user_api_get_by_id.return_value = None
        mock_data_api_change_owner.return_value = None

        # Act
        response = RequestMock.do_request_patch(
            data_rest_views.DataChangeOwner.as_view(),
            user_request,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataPermissions(SimpleTestCase):
    """TestDataPermissions"""

    @patch.object(Data, "get_by_id")
    def test_superuser_returns_http_200(self, get_by_id):
        """test_superuser_returns_http_200

        Args:
            get_by_id:

        Returns:

        """
        mock_user = create_mock_user(1, is_superuser=True)
        mock_data = Data(user_id="1")
        get_by_id.return_value = mock_data

        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            mock_user,
            data={"ids": f'["{mock_data.id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Data, "get_by_id")
    def test_authenticated_returns_http_200(self, get_by_id):
        """test_authenticated_returns_http_200

        Args:
            get_by_id:

        Returns:

        """
        mock_user = create_mock_user(1)
        mock_data = Data(user_id="1")
        get_by_id.return_value = mock_data

        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            mock_user,
            data={"ids": f'["{mock_data.id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Data, "get_by_id")
    def test_staff_returns_http_200(self, get_by_id):
        """test_staff_returns_http_200

        Args:
            get_by_id:

        Returns:

        """
        mock_user = create_mock_user(1, is_staff=True)
        mock_data = Data(user_id="1")
        get_by_id.return_value = mock_data

        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            mock_user,
            data={"ids": f'["{mock_data.id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Data, "get_by_id")
    def test_get_returns_200_for_anonymous(self, get_by_id):
        """test_get_returns_200_for_anonymous

        Args:
            get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("999", is_anonymous=True)
        mock_data = Data(user_id="1")
        get_by_id.return_value = mock_data

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            mock_user,
            data={"ids": '["1"]'},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataMigrationPermission(SimpleTestCase):
    """TestDataMigrationPermission"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_validation_returns_http_403(self):
        """test_anonymous_validation_returns_http_403

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1, is_anonymous=True)

        # Act
        response = RequestMock.do_request_post(
            data_validation.as_view(),
            mock_user,
            param={"pk": self.fake_id},
            data={"data": f'["{self.fake_id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_validation_returns_http_403(self):
        """test_staff_validation_returns_http_403

        Returns:

        """
        # Arrange
        request_user = create_mock_user(1, is_staff=True)

        # Act
        response = RequestMock.do_request_post(
            data_validation.as_view(),
            request_user,
            param={"pk": self.fake_id},
            data={"data": f'["{self.fake_id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_api, "migrate_data_list")
    def test_admin_validation_returns_http_200(self, migration):
        """test_admin_validation_returns_http_200

        Args:
            migration:

        Returns:

        """
        # Arrange
        migration.return_value = "123"
        request_user = create_mock_user(1, is_superuser=True)

        # Act
        response = RequestMock.do_request_post(
            data_validation.as_view(),
            request_user,
            param={"pk": self.fake_id},
            data={"data": f'["{self.fake_id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_migration_returns_http_403(self):
        """test_anonymous_migration_returns_http_403

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1, is_anonymous=True)

        # Act
        response = RequestMock.do_request_post(
            data_migration.as_view(),
            mock_user,
            param={"pk": self.fake_id},
            data={"data": f'["{self.fake_id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_migration_returns_http_403(self):
        """test_staff_migration_returns_http_403

        Returns:

        """
        # Arrange
        request_user = create_mock_user(1, is_staff=True)

        # Act
        response = RequestMock.do_request_post(
            data_migration.as_view(),
            request_user,
            param={"pk": self.fake_id},
            data={"data": f'["{self.fake_id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_api, "migrate_data_list")
    def test_admin_migration_returns_http_200(self, migration):
        """test_admin_migration_returns_http_200

        Args:
            migration:

        Returns:

        """
        # Arrange
        migration.return_value = "123"
        request_user = create_mock_user(1, is_superuser=True)

        # Act
        response = RequestMock.do_request_post(
            data_migration.as_view(),
            request_user,
            param={"pk": self.fake_id},
            data={"data": f'["{self.fake_id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetTaskProgressPermission(SimpleTestCase):
    """TestGetTaskProgressPermission"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.task_id = "123"

    def test_anonymous_get_task_progress_returns_http_403(self):
        """test_anonymous_get_task_progress_returns_http_403

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1, is_anonymous=True)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.GetTaskProgress.as_view(),
            mock_user,
            param={"task_id": self.task_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_task_progress_returns_http_403(self):
        """test_user_get_task_progress_returns_http_403

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.GetTaskProgress.as_view(),
            mock_user,
            param={"task_id": self.task_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.data.tasks.get_task_progress")
    def test_admin_get_task_progress_returns_http_200(
        self, mock_get_task_progress
    ):
        """test_admin_get_task_progress_returns_http_200

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1, is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.GetTaskProgress.as_view(),
            mock_user,
            param={"task_id": self.task_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGetTaskResultPermission(SimpleTestCase):
    """TestGetTaskResultPermission"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.task_id = "123"

    def test_anonymous_get_task_result_returns_http_403(self):
        """test_anonymous_get_task_result_returns_http_403

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(None, is_anonymous=True)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.GetTaskResult.as_view(),
            mock_user,
            param={"task_id": self.task_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_task_result_returns_http_403(self):
        """test_user_get_task_result_returns_http_403

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.GetTaskResult.as_view(),
            mock_user,
            param={"task_id": self.task_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.data.tasks.get_task_result")
    def test_admin_get_task_result_returns_http_200(
        self, mock_get_task_result
    ):
        """test_admin_get_task_result_returns_http_200

        Returns:

        """
        # Arrange
        mock_user = create_mock_user(1, is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.GetTaskResult.as_view(),
            mock_user,
            param={"task_id": self.task_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
