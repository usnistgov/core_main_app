""" Permissions Test for Workspace Rest API
"""
from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.response import Response

from core_main_app.components.workspace import api as workspace_api
from core_main_app.rest.workspace import views as workspace_rest_views
from core_main_app.rest.workspace.serializers import WorkspaceSerializer
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestGetWorkspaceDetail(SimpleTestCase):
    """Test Get Workspace Detail"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceDetail.as_view(),
            None,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(workspace_api, "get_by_id")
    @patch.object(WorkspaceSerializer, "data")
    def test_staff_returns_http_200(
        self, mock_workspace_api_get_by_id, mock_data_serializer_data
    ):
        """test_staff_returns_http_200

        Args:
            mock_workspace_api_get_by_id:
            mock_data_serializer_data:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_api_get_by_id.return_value = None
        mock_data_serializer_data.return_value = []

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceDetail.as_view(),
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(workspace_api, "get_by_id")
    @patch.object(WorkspaceSerializer, "data")
    def test_authenticated_returns_http_200(
        self, mock_workspace_api_get_by_id, mock_data_serializer_data
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_workspace_api_get_by_id:
            mock_data_serializer_data:
        """
        # Context
        user = create_mock_user("1")
        mock_workspace_api_get_by_id.return_value = None
        mock_data_serializer_data.return_value = []

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceDetail.as_view(),
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDeleteWorkspace(SimpleTestCase):
    """Test Delete Workspace"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_delete(
            workspace_rest_views.WorkspaceDetail.as_view(),
            None,
            param={"pk": 0},
        )
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(workspace_api, "get_by_id")
    @patch.object(workspace_api, "delete")
    def test_staff_returns_http_204(
        self, mock_workspace_api_get_by_id, mock_workspace_api_delete
    ):
        """test_staff_returns_http_204

        Args:
            mock_workspace_api_get_by_id:
            mock_workspace_api_delete:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_api_get_by_id.return_value = None
        mock_workspace_api_delete.returns_value = None

        # Act
        response = RequestMock.do_request_delete(
            workspace_rest_views.WorkspaceDetail.as_view(),
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(workspace_api, "get_by_id")
    @patch.object(workspace_api, "delete")
    def test_authenticated_returns_http_204(
        self, mock_workspace_api_get_by_id, mock_workspace_api_delete
    ):
        """test_authenticated_returns_http_204

        Args:
            mock_workspace_api_get_by_id:
            mock_workspace_api_delete:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_workspace_api_get_by_id.return_value = None
        mock_workspace_api_delete.return_value = None

        # Act
        response = RequestMock.do_request_delete(
            workspace_rest_views.WorkspaceDetail.as_view(),
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestGetWorkspace(SimpleTestCase):
    """Test Get Workspace"""

    def test_get_anonymous_returns_http_403(self):
        """test_get_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceList.as_view(), None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(workspace_api, "get_all_by_owner")
    @patch.object(WorkspaceSerializer, "data")
    def test_get_staff_returns_http_200(
        self, mock_workspace_api_get_all_by_owner, mock_data_serializer_data
    ):
        """test_get_staff_returns_http_200

        Args:
            mock_workspace_api_get_all_by_owner:
            mock_data_serializer_data:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_api_get_all_by_owner.return_value = None
        mock_data_serializer_data.return_value = []

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(workspace_api, "get_all_by_owner")
    @patch.object(WorkspaceSerializer, "data")
    def test_get_authenticated_returns_http_200(
        self, mock_workspace_api_get_all_by_owner, mock_data_serializer_data
    ):
        """test_get_authenticated_returns_http_200

        Args:
            mock_workspace_api_get_all_by_owner:
            mock_data_serializer_data:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_workspace_api_get_all_by_owner.return_value = None
        mock_data_serializer_data.return_value = []

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCreateWorkspace(SimpleTestCase):
    """Test Create Workspace"""

    def test_post_anonymous_returns_http_403(self):
        """test_post_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_post(
            workspace_rest_views.WorkspaceList.as_view(),
            None,
            data={"title": "title 1"},
        )
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(WorkspaceSerializer, "data")
    @patch.object(WorkspaceSerializer, "is_valid")
    @patch.object(WorkspaceSerializer, "save")
    def test_post_staff_returns_http_201(
        self,
        mock_data_serializer_save,
        mock_data_serializer_is_valid,
        mock_data_serializer_data,
    ):
        """test_post_staff_returns_http_201

        Args:
            mock_data_serializer_save:
            mock_data_serializer_is_valid:
            mock_data_serializer_data:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_data_serializer_is_valid.return_value = True
        mock_data_serializer_save.return_value = None
        mock_data_serializer_data.return_value = []

        # Act
        response = RequestMock.do_request_post(
            workspace_rest_views.WorkspaceList.as_view(),
            user,
            data={"title": "title 1"},
        )
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(WorkspaceSerializer, "data")
    @patch.object(WorkspaceSerializer, "is_valid")
    @patch.object(WorkspaceSerializer, "save")
    def test_post_authenticated_returns_http_201(
        self,
        mock_data_serializer_save,
        mock_data_serializer_is_valid,
        mock_data_serializer_data,
    ):
        """test_post_authenticated_returns_http_201

        Args:
            mock_data_serializer_save:
            mock_data_serializer_is_valid:
            mock_data_serializer_data:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_data_serializer_is_valid.return_value = True
        mock_data_serializer_save.return_value = None
        mock_data_serializer_data.return_value = []

        # Act
        response = RequestMock.do_request_post(
            workspace_rest_views.WorkspaceList.as_view(),
            user,
            data={"title": "title 1"},
        )
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestWorkspaceReadAccess(SimpleTestCase):
    """Test Workspace Read Access"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_read_access, None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(workspace_api, "get_all_workspaces_with_read_access_by_user")
    @patch.object(workspace_rest_views, "_list_of_workspaces_to_response")
    def test_staff_returns_http_200(
        self,
        mock_workspace_rest_views__list_of_workspaces_to_response,
        mock_workspace_api_get_all_workspaces_with_read_access_by_user,
    ):
        """test_staff_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_workspaces_to_response:
            mock_workspace_api_get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_api_get_all_workspaces_with_read_access_by_user.return_value = (
            None
        )
        mock_workspace_rest_views__list_of_workspaces_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_read_access, user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(workspace_api, "get_all_workspaces_with_read_access_by_user")
    @patch.object(workspace_rest_views, "_list_of_workspaces_to_response")
    def test_authenticated_returns_http_200(
        self,
        mock_workspace_rest_views__list_of_workspaces_to_response,
        mock_workspace_api_get_all_workspaces_with_read_access_by_user,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_workspaces_to_response:
            mock_workspace_api_get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_workspace_api_get_all_workspaces_with_read_access_by_user.return_value = (
            None
        )
        mock_workspace_rest_views__list_of_workspaces_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_read_access, user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWorkspaceWriteAccess(SimpleTestCase):
    """Test Workspace Write Access"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_write_access, None
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(
        workspace_api, "get_all_workspaces_with_write_access_by_user"
    )
    @patch.object(workspace_rest_views, "_list_of_workspaces_to_response")
    def test_staff_returns_http_200(
        self,
        mock_workspace_rest_views__list_of_workspaces_to_response,
        mock_workspace_api_get_all_workspaces_with_write_access_by_user,
    ):
        """test_staff_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_workspaces_to_response:
            mock_workspace_api_get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_api_get_all_workspaces_with_write_access_by_user.return_value = (
            None
        )
        mock_workspace_rest_views__list_of_workspaces_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_write_access, user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(
        workspace_api, "get_all_workspaces_with_write_access_by_user"
    )
    @patch.object(workspace_rest_views, "_list_of_workspaces_to_response")
    def test_authenticated_returns_http_200(
        self,
        mock_workspace_rest_views__list_of_workspaces_to_response,
        mock_workspace_api_get_all_workspaces_with_write_access_by_user,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_workspaces_to_response:
            mock_workspace_api_get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_workspace_api_get_all_workspaces_with_write_access_by_user.return_value = (
            None
        )
        mock_workspace_rest_views__list_of_workspaces_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_write_access, user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWorkspaceIsPublic(SimpleTestCase):
    """Test Workspace Is Public"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.is_workspace_public, None, param={"pk": 0}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(workspace_api, "get_by_id")
    @patch.object(workspace_api, "is_workspace_public")
    def test_staff_returns_http_200(
        self,
        mock_workspace_api_get_by_id,
        mock_workspace_api_is_workspace_public,
    ):
        """test_staff_returns_http_200

        Args:
            mock_workspace_api_get_by_id:
            mock_workspace_api_is_workspace_public:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_api_get_by_id.return_value = None
        mock_workspace_api_is_workspace_public.return_value = None

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.is_workspace_public, user, param={"pk": 0}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(workspace_api, "get_by_id")
    @patch.object(workspace_api, "is_workspace_public")
    def test_authenticated_returns_http_200(
        self,
        mock_workspace_api_get_by_id,
        mock_workspace_api_is_workspace_public,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_workspace_api_get_by_id:
            mock_workspace_api_is_workspace_public:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_workspace_api_get_by_id.return_value = None
        mock_workspace_api_is_workspace_public.return_value = None

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.is_workspace_public, user, param={"pk": 0}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWorkspaceSetPublic(SimpleTestCase):
    """Test Workspace Set Public"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_public, None, param={"pk": 0}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(workspace_api, "get_by_id")
    @patch.object(workspace_api, "set_workspace_public")
    def test_staff_returns_http_200(
        self,
        mock_workspace_api_get_by_id,
        mock_workspace_api_set_workspace_public,
    ):
        """test_staff_returns_http_200

        Args:
            mock_workspace_api_get_by_id:
            mock_workspace_api_set_workspace_public:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_api_get_by_id.return_value = None
        mock_workspace_api_set_workspace_public.return_value = None

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_public, user, param={"pk": 0}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(workspace_api, "get_by_id")
    @patch.object(workspace_api, "set_workspace_public")
    def test_authenticated_returns_http_200(
        self,
        mock_workspace_api_get_by_id,
        mock_workspace_api_set_workspace_public,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_workspace_api_get_by_id:
            mock_workspace_api_set_workspace_public:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_workspace_api_get_by_id.return_value = None
        mock_workspace_api_set_workspace_public.return_value = None

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_public, user, param={"pk": 0}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWorkspaceSetPrivate(SimpleTestCase):
    """Test Workspace Set Private"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_private, None, param={"pk": 0}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(workspace_api, "get_by_id")
    @patch.object(workspace_api, "set_workspace_private")
    def test_staff_returns_http_200(
        self,
        mock_workspace_api_get_by_id,
        mock_workspace_api_set_workspace_private,
    ):
        """test_staff_returns_http_200

        Args:
            mock_workspace_api_get_by_id:
            mock_workspace_api_set_workspace_private:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_api_get_by_id.return_value = None
        mock_workspace_api_set_workspace_private.return_value = None

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_private, user, param={"pk": 0}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(workspace_api, "get_by_id")
    @patch.object(workspace_api, "set_workspace_private")
    def test_authenticated_returns_http_200(
        self,
        mock_workspace_api_get_by_id,
        mock_workspace_api_set_workspace_private,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_workspace_api_get_by_id:
            mock_workspace_api_set_workspace_private:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_workspace_api_get_by_id.return_value = None
        mock_workspace_api_set_workspace_private.return_value = None

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_private, user, param={"pk": 0}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWorkspaceListUserCanRead(SimpleTestCase):
    """Test Workspace List User Can read"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_read_workspace,
            None,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(workspace_rest_views, "_list_of_users_or_groups_to_response")
    def test_staff_returns_http_200(
        self, mock_workspace_rest_views__list_of_users_or_groups_to_response
    ):
        """test_staff_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_users_or_groups_to_response:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_rest_views__list_of_users_or_groups_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_read_workspace,
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(workspace_rest_views, "_list_of_users_or_groups_to_response")
    def test_authenticated_returns_http_200(
        self, mock_workspace_rest_views__list_of_users_or_groups_to_response
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_users_or_groups_to_response:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_workspace_rest_views__list_of_users_or_groups_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_read_workspace,
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWorkspaceListUserCanWrite(SimpleTestCase):
    """Test Workspace List User Can Write"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_write_workspace,
            None,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(workspace_rest_views, "_list_of_users_or_groups_to_response")
    def test_staff_returns_http_200(
        self, mock_workspace_rest_views__list_of_users_or_groups_to_response
    ):
        """test_staff_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_users_or_groups_to_response:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_rest_views__list_of_users_or_groups_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_write_workspace,
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(workspace_rest_views, "_list_of_users_or_groups_to_response")
    def test_authenticated_returns_http_200(
        self, mock_workspace_rest_views__list_of_users_or_groups_to_response
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_users_or_groups_to_response:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_workspace_rest_views__list_of_users_or_groups_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_write_workspace,
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWorkspaceListGroupCanRead(SimpleTestCase):
    """Test Workspace List Group Can read"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_read_workspace,
            None,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(workspace_rest_views, "_list_of_users_or_groups_to_response")
    def test_staff_returns_http_200(
        self, mock_workspace_rest_views__list_of_users_or_groups_to_response
    ):
        """test_staff_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_users_or_groups_to_response:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_rest_views__list_of_users_or_groups_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_read_workspace,
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(workspace_rest_views, "_list_of_users_or_groups_to_response")
    def test_authenticated_returns_http_200(
        self, mock_workspace_rest_views__list_of_users_or_groups_to_response
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_users_or_groups_to_response:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_workspace_rest_views__list_of_users_or_groups_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_read_workspace,
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWorkspaceListGroupCanWrite(SimpleTestCase):
    """Test Workspace List Group Can Write"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_write_workspace,
            None,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(workspace_rest_views, "_list_of_users_or_groups_to_response")
    def test_staff_returns_http_200(
        self, mock_workspace_rest_views__list_of_users_or_groups_to_response
    ):
        """test_staff_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_users_or_groups_to_response:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_workspace_rest_views__list_of_users_or_groups_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_write_workspace,
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(workspace_rest_views, "_list_of_users_or_groups_to_response")
    def test_authenticated_returns_http_200(
        self, mock_workspace_rest_views__list_of_users_or_groups_to_response
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_workspace_rest_views__list_of_users_or_groups_to_response:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_workspace_rest_views__list_of_users_or_groups_to_response.return_value = Response(
            status=status.HTTP_200_OK
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_write_workspace,
            user,
            param={"pk": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAddUserReadRightToWorkspace(SimpleTestCase):
    """Test Add User Read Right To Workspace"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_read_right_to_workspace,
            None,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_staff_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_staff_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_read_right_to_workspace,
            user,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_authenticated_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_read_right_to_workspace,
            user,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAddUserWriteRightToWorkspace(SimpleTestCase):
    """Test Add User Write Right To Workspace"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_write_right_to_workspace,
            None,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_staff_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_staff_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_write_right_to_workspace,
            user,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_authenticated_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_write_right_to_workspace,
            user,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAddGroupReadRightToWorkspace(SimpleTestCase):
    """Test Add Group Read Right To Workspace"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_read_right_to_workspace,
            None,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_staff_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_staff_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_read_right_to_workspace,
            user,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_authenticated_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_read_right_to_workspace,
            user,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAddGroupWriteRightToWorkspace(SimpleTestCase):
    """Test Add Group Write Right To Workspace"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_write_right_to_workspace,
            None,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_staff_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_staff_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_write_right_to_workspace,
            user,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_authenticated_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_write_right_to_workspace,
            user,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRemoveUserReadRightToWorkspace(SimpleTestCase):
    """Test Remove User Read Right To Workspace"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_read_right_to_workspace,
            None,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_read_right_to_workspace,
            user,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_authenticated_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_read_right_to_workspace,
            user,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRemoveUserWriteRightToWorkspace(SimpleTestCase):
    """Test Remove User Write Right To Workspace"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_write_right_to_workspace,
            None,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_staff_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_staff_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_write_right_to_workspace,
            user,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_authenticated_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_write_right_to_workspace,
            user,
            param={"pk": 0, "user_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRemoveGroupReadRightToWorkspace(SimpleTestCase):
    """Test Remove Group Read Right To Workspace"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_read_right_to_workspace,
            None,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_staff_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_staff_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_read_right_to_workspace,
            user,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_authenticated_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1")
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_read_right_to_workspace,
            user,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRemoveGroupWriteRightToWorkspace(SimpleTestCase):
    """Test Remove Group Write Right To Workspace"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_write_right_to_workspace,
            None,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_staff_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_staff_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        user = create_mock_user("1", is_staff=True)
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_write_right_to_workspace,
            user,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(
        workspace_rest_views,
        "_add_or_remove_to_user_or_group_right_to_workspace",
    )
    def test_authenticated_returns_http_200(
        self,
        mock_add_or_remove_to_user_or_group_right_to_workspace,
    ):
        """test_authenticated_returns_http_200

        Args:
            mock_add_or_remove_to_user_or_group_right_to_workspace:

        Returns:

        """
        # Context
        mock_add_or_remove_to_user_or_group_right_to_workspace.return_value = (
            Response(status=status.HTTP_200_OK)
        )
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_write_right_to_workspace,
            user,
            param={"pk": 0, "group_id": 0},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
