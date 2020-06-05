""" Authentication tests for Data REST API
"""
from django.test import SimpleTestCase
from mock import Mock
from mock.mock import patch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.workspace import api as workspace_api
from core_main_app.rest.data import views as data_rest_views
from core_main_app.rest.data.abstract_views import AbstractExecuteLocalQueryView
from core_main_app.rest.data.admin_serializers import AdminDataSerializer
from core_main_app.rest.data.serializers import (
    DataSerializer,
    DataWithTemplateInfoSerializer,
)
from core_main_app.rest.data.views import Validation as data_validation
from core_main_app.rest.data.views import Migration as data_migration
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestDataListPostPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_post(data_rest_views.DataList.as_view(), None)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(DataSerializer, "is_valid")
    @patch.object(DataSerializer, "save")
    @patch.object(DataSerializer, "data")
    def test_authenticated_returns_http_201(
        self, data_serializer_data, data_serializer_save, data_serializer_valid
    ):
        data_serializer_valid.return_value = True
        data_serializer_save.return_value = None
        data_serializer_data.return_value = {}

        mock_user = create_mock_user("1")

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
        data_serializer_valid.return_value = True
        data_serializer_save.return_value = None
        data_serializer_data.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            data_rest_views.DataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestDataListGetPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(data_rest_views.DataList.as_view(), None)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(Data, "get_all_by_user_id")
    def test_authenticated_returns_http_200(self, data_get_all_by_user):
        data_get_all_by_user.return_value = {}

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Data, "get_all_by_user_id")
    def test_staff_returns_http_200(self, data_get_all_by_user):
        data_get_all_by_user.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAdminDataListPostPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_post(
            data_rest_views.AdminDataList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")
        response = RequestMock.do_request_post(
            data_rest_views.AdminDataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_http_403(self):
        mock_user = create_mock_user("1", is_staff=True)
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
        data_serializer_valid.return_value = True
        data_serializer_save.return_value = None
        data_serializer_data.return_value = {}

        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_post(
            data_rest_views.AdminDataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestAdminDataListGetPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            data_rest_views.AdminDataList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")
        response = RequestMock.do_request_get(
            data_rest_views.AdminDataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_http_403(self):
        mock_user = create_mock_user("1", is_staff=True)
        response = RequestMock.do_request_get(
            data_rest_views.AdminDataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(Data, "get_all_by_user_id")
    def test_superuser_returns_http_200(self, data_get_all_by_user):
        data_get_all_by_user.return_value = {}

        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_get(
            data_rest_views.AdminDataList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataListByWorkspaceGetPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            data_rest_views.DataListByWorkspace.as_view(),
            None,
            param={"workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_api, "get_all_by_workspace")
    def test_authenticated_returns_http_200(self, data_get_all_by_workspace):
        data_get_all_by_workspace.return_value = {}

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            data_rest_views.DataListByWorkspace.as_view(),
            mock_user,
            param={"workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_all_by_workspace")
    def test_staff_returns_http_200(self, data_get_all_by_workspace):
        data_get_all_by_workspace.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.DataListByWorkspace.as_view(),
            mock_user,
            param={"workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataDetailGetPermissions(SimpleTestCase):
    @patch.object(DataSerializer, "data")
    @patch.object(data_api, "get_by_id")
    def test_anonymous_returns_http_200(
        self, mock_data_api_get_by_id, mock_data_serializer_data
    ):
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
        mock_data_api_get_by_id.return_value = None
        mock_data_serializer_data.return_value = []

        mock_user = create_mock_user("1")
        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(DataSerializer, "data")
    @patch.object(data_api, "get_by_id")
    def test_staff_returns_http_200(
        self, mock_data_api_get_by_id, mock_data_serializer_data
    ):
        mock_data_api_get_by_id.return_value = None
        mock_data_serializer_data.return_value = []

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataDetailDeletePermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_delete(
            data_rest_views.DataDetail.as_view(), None, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_api, "delete")
    @patch.object(data_api, "get_by_id")
    def test_authenticated_returns_http_204(
        self, mock_data_api_get_by_id, mock_data_api_delete
    ):
        mock_data_api_get_by_id.return_value = None
        mock_data_api_delete.return_value = None

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(data_api, "delete")
    @patch.object(data_api, "get_by_id")
    def test_staff_returns_http_204(
        self, mock_data_api_get_by_id, mock_data_api_delete
    ):
        mock_data_api_get_by_id.return_value = None
        mock_data_api_delete.return_value = None

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_delete(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestDataDetailPatchPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
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
        mock_data_api_get_by_id.return_value = []
        mock_data_serializer_is_valid.return_value = True
        mock_data_serializer_save.return_valie = None
        mock_data_serializer_data.return_value = []

        mock_user = create_mock_user("1")

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
        mock_data_api_get_by_id.return_value = []
        mock_data_serializer_is_valid.return_value = True
        mock_data_serializer_save.return_valie = None
        mock_data_serializer_data.return_value = []

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataDownloadGetPermissions(SimpleTestCase):
    @patch.object(data_api, "get_by_id")
    def test_anonymous_returns_http_200(self, mock_data_api_get_by_id):
        data_object = Mock()
        data_object.xml_content = "<tag attr='attr_val'>tag_val</tag>"
        data_object.title = "mock.xml"

        mock_data_api_get_by_id.return_value = data_object

        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(), None, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_by_id")
    def test_authenticated_returns_http_200(self, mock_data_api_get_by_id):
        data_object = Mock()
        data_object.xml_content = "<tag attr='attr_val'>tag_val</tag>"
        data_object.title = "mock.xml"

        mock_data_api_get_by_id.return_value = data_object

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_by_id")
    def test_staff_returns_http_200(self, mock_data_api_get_by_id):
        data_object = Mock()
        data_object.xml_content = "<tag attr='attr_val'>tag_val</tag>"
        data_object.title = "mock.xml"

        mock_data_api_get_by_id.return_value = data_object

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(), mock_user, param={"pk": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataGetFullGetPermissions(SimpleTestCase):
    @patch.object(DataWithTemplateInfoSerializer, "data")
    @patch.object(data_api, "get_by_id")
    def test_anonymous_returns_http_200(
        self, mock_data_api_get_by_id, mock_data_with_template_serializer_data
    ):
        mock_data_api_get_by_id.return_value = None
        mock_data_with_template_serializer_data.return_value = []

        response = RequestMock.do_request_get(
            data_rest_views.get_by_id_with_template_info, None, data={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(DataWithTemplateInfoSerializer, "data")
    @patch.object(data_api, "get_by_id")
    def test_authenticated_returns_http_200(
        self, mock_data_api_get_by_id, mock_data_with_template_serializer_data
    ):
        mock_data_api_get_by_id.return_value = None
        mock_data_with_template_serializer_data.return_value = []

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            data_rest_views.get_by_id_with_template_info, mock_user, data={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(DataWithTemplateInfoSerializer, "data")
    @patch.object(data_api, "get_by_id")
    def test_staff_returns_http_200(
        self, mock_data_api_get_by_id, mock_data_with_template_serializer_data
    ):
        mock_data_api_get_by_id.return_value = None
        mock_data_with_template_serializer_data.return_value = []

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.get_by_id_with_template_info, mock_user, data={"id": 0}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataLocalQueryGetPermissions(SimpleTestCase):
    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_anonymous_returns_http_200(self, mock_abstract_local_query_execute_query):
        mock_abstract_local_query_execute_query.return_value = Response(
            status=HTTP_200_OK
        )

        response = RequestMock.do_request_get(
            data_rest_views.ExecuteLocalQueryView.as_view(), None, data={"query": "{}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_authenticated_returns_http_200(
        self, mock_abstract_local_query_execute_query
    ):
        mock_abstract_local_query_execute_query.return_value = Response(
            status=HTTP_200_OK
        )

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_staff_returns_http_200(self, mock_abstract_local_query_execute_query):
        mock_abstract_local_query_execute_query.return_value = Response(
            status=HTTP_200_OK
        )

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataLocalQueryPostPermissions(SimpleTestCase):
    @patch.object(data_api, "execute_query")
    def test_anonymous_returns_http_200(self, mock_data_api_execute_query):
        mock_data_api_execute_query.return_value = []

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), None, data={"query": "{}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "execute_query")
    def test_authenticated_returns_http_200(self, mock_data_api_execute_query):
        mock_data_api_execute_query.return_value = []

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "execute_query")
    def test_staff_returns_http_200(self, mock_data_api_execute_query):
        mock_data_api_execute_query.return_value = []

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataKeywordQueryGetPermissions(SimpleTestCase):
    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_anonymous_returns_http_200(self, mock_abstract_local_query_execute_query):
        mock_abstract_local_query_execute_query.return_value = Response(
            status=HTTP_200_OK
        )

        response = RequestMock.do_request_get(
            data_rest_views.ExecuteLocalQueryView.as_view(), None, data={"query": "{}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_authenticated_returns_http_200(
        self, mock_abstract_local_query_execute_query
    ):
        mock_abstract_local_query_execute_query.return_value = Response(
            status=HTTP_200_OK
        )

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(AbstractExecuteLocalQueryView, "execute_query")
    def test_staff_returns_http_200(self, mock_abstract_local_query_execute_query):
        mock_abstract_local_query_execute_query.return_value = Response(
            status=HTTP_200_OK
        )

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataKeywordQueryPostPermissions(SimpleTestCase):
    @patch.object(data_api, "execute_query")
    def test_anonymous_returns_http_200(self, mock_data_api_execute_query):
        mock_data_api_execute_query.return_value = []

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalKeywordQueryView.as_view(),
            None,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "execute_query")
    def test_authenticated_returns_http_200(self, mock_data_api_execute_query):
        mock_data_api_execute_query.return_value = []

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalKeywordQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "execute_query")
    def test_staff_returns_http_200(self, mock_data_api_execute_query):
        mock_data_api_execute_query.return_value = []

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalKeywordQueryView.as_view(),
            mock_user,
            data={"query": "{}"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataAssignPatchPermissions(SimpleTestCase):
    @patch.object(data_api, "assign")
    @patch.object(workspace_api, "get_by_id")
    @patch.object(data_api, "get_by_id")
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
        mock_data_api_get_by_id.return_value = None
        mock_workspace_api_get_by_id.return_value = None
        mock_data_api_assign.return_value = None

        mock_user = create_mock_user("1")

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
        mock_data_api_get_by_id.return_value = None
        mock_workspace_api_get_by_id.return_value = None
        mock_data_api_assign.return_value = None

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            data_rest_views.DataAssign.as_view(),
            mock_user,
            param={"pk": 0, "workspace_id": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataChangeOwnerPatchPermissions(SimpleTestCase):
    @patch.object(data_api, "change_owner")
    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Data, "get_by_id")
    def test_anonymous_returns_http_403(
        self,
        mock_data_api_get_by_id,
        mock_user_api_get_by_id,
        mock_data_api_change_owner,
    ):
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
        mock_data_api_get_by_id.return_value = None
        mock_user_api_get_by_id.return_value = None
        mock_data_api_change_owner.return_value = None

        mock_user = create_mock_user("1")

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
        # Arrange
        # is_staff to access the view
        # is_superuser to be able to change the owner
        user_request = create_mock_user("1", is_staff=True, is_superuser=True)
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
    @patch.object(Data, "get_by_id")
    def test_superuser_returns_http_200(self, get_by_id):
        mock_user = create_mock_user("1", is_superuser=True)
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
        mock_user = create_mock_user("1")
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
        mock_user = create_mock_user("1", is_staff=True)
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
        # Arrange
        mock_user = create_mock_user("999", is_anonymous=True)
        mock_data = Data(user_id="1")
        get_by_id.return_value = mock_data

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(), mock_user, data={"ids": '["1"]'}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataMigrationPermission(SimpleTestCase):
    def setUp(self):
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_validation_returns_http_403(self):
        # Arrange
        mock_user = create_mock_user("1", is_anonymous=True)

        # Act
        response = RequestMock.do_request_post(
            data_validation.as_view(),
            mock_user,
            param={"pk": self.fake_id},
            data={"data": f'["{self.fake_id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_validation_returns_http_403(self):
        # Arrange
        request_user = create_mock_user("1", is_staff=True)

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
        # Arrange
        migration.return_value = "123"
        request_user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_post(
            data_validation.as_view(),
            request_user,
            param={"pk": self.fake_id},
            data={"data": f'["{self.fake_id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_migration_returns_http_403(self):
        # Arrange
        mock_user = create_mock_user("1", is_anonymous=True)

        # Act
        response = RequestMock.do_request_post(
            data_migration.as_view(),
            mock_user,
            param={"pk": self.fake_id},
            data={"data": f'["{self.fake_id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_migration_returns_http_403(self):
        # Arrange
        request_user = create_mock_user("1", is_staff=True)

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
        # Arrange
        migration.return_value = "123"
        request_user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_post(
            data_migration.as_view(),
            request_user,
            param={"pk": self.fake_id},
            data={"data": f'["{self.fake_id}"]'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
