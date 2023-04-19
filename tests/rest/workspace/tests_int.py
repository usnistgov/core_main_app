""" Integration Test for Workspace Rest API
"""

from rest_framework import status
from tests.components.group.fixtures.fixtures import GroupFixtures
from tests.components.user.fixtures.fixtures import UserFixtures
from tests.components.workspace.fixtures.fixtures import WorkspaceFixtures

from core_main_app.components.workspace import api as workspace_api
from core_main_app.rest.workspace import views as workspace_rest_views
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)
from core_main_app.utils.tests_tools.RequestMock import RequestMock

TITLE_1 = "title 1"
TITLE_2 = "title 2"
TITLE_3 = "title 3"

FAKE_WORKSPACE_ID = -1


class TestWorkspaceDetail(IntegrationTransactionTestCase):
    """Test Workspace Detail"""

    def test_get_returns_http_200(self):
        """test_get_returns_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user()

        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceDetail.as_view(),
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_workspace(self):
        """test_get_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user()

        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceDetail.as_view(),
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.data["title"], workspace.title)

    def test_get_wrong_id_returns_http_404(self):
        """test_get_wrong_id_returns_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user()

        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceDetail.as_view(),
            user,
            param={"pk": FAKE_WORKSPACE_ID},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_wrong_id_returns_http_404(self):
        """test_delete_wrong_id_returns_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user()

        # Act
        response = RequestMock.do_request_delete(
            workspace_rest_views.WorkspaceDetail.as_view(),
            user,
            param={"pk": FAKE_WORKSPACE_ID},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_returns_http_204(self):
        """test_delete_returns_http_204

        Returns:

        """
        # Context
        user = UserFixtures().create_user()

        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_delete(
            workspace_rest_views.WorkspaceDetail.as_view(),
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_workspace(self):
        """test_delete_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user()
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        self.assertEqual(len(workspace_api.get_all_by_owner(user)), 1)

        # Act
        RequestMock.do_request_delete(
            workspace_rest_views.WorkspaceDetail.as_view(),
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(workspace_api.get_all_by_owner(user)), 0)

    def test_delete_workspace_not_owner(self):
        """test_delete_workspace_not_owner

        Returns:

        """
        # Context
        user = UserFixtures().create_user()
        user2 = UserFixtures().create_user(username="other")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        self.assertEqual(len(workspace_api.get_all_by_owner(user)), 1)

        # Act
        response = RequestMock.do_request_delete(
            workspace_rest_views.WorkspaceDetail.as_view(),
            user2,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestWorkspaceList(IntegrationTransactionTestCase):
    """Test Workspace List"""

    def test_get_returns_http_200(self):
        """test_get_returns_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user()

        WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        WorkspaceFixtures().create_workspace(user.id, TITLE_2)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_user_workspaces(self):
        """test_get_all_user_workspaces

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        other_user = UserFixtures().create_user(username="user2")

        WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        WorkspaceFixtures().create_workspace(user.id, TITLE_2)
        WorkspaceFixtures().create_workspace(other_user.id, TITLE_3)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceList.as_view(), user
        )

        # Assert
        self.assertEqual(len(response.data), 2)

    def test_get_all_workspaces_as_admin(self):
        """test_get_all_workspaces_as_admin

        Returns:

        """
        # Context
        user = UserFixtures().create_super_user(username="user1")
        other_user = UserFixtures().create_user(username="user2")

        WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        WorkspaceFixtures().create_workspace(user.id, TITLE_2)
        WorkspaceFixtures().create_workspace(other_user.id, TITLE_3)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.WorkspaceList.as_view(), user
        )

        # Assert
        self.assertEqual(len(response.data), 3)

    def test_post_returns_http_201(self):
        """test_post_returns_http_201

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        mock_data = {"title": "title 1"}

        # Act
        response = RequestMock.do_request_post(
            workspace_rest_views.WorkspaceList.as_view(), user, data=mock_data
        )
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_create_workspace(self):
        """test_post_create_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        mock_data = {"title": TITLE_1}

        # Act
        RequestMock.do_request_post(
            workspace_rest_views.WorkspaceList.as_view(), user, data=mock_data
        )

        # Assert
        workspace = workspace_api.get_all_by_owner(user)
        self.assertEqual(len(workspace), 1)
        self.assertEqual(workspace[0].title, TITLE_1)
        self.assertEqual(workspace[0].owner, str(user.id))

    def test_post_create_workspace_with_owner(self):
        """test_post_create_workspace_with_owner

        Returns:

        """
        # Context
        fake_user_id = 123456
        user = UserFixtures().create_user(username="user1")
        mock_data = {"title": TITLE_1, "owner": fake_user_id}

        # Act
        response = RequestMock.do_request_post(
            workspace_rest_views.WorkspaceList.as_view(), user, data=mock_data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        workspace = workspace_api.get_all_by_owner(user)
        self.assertEqual(len(workspace), 1)
        self.assertEqual(workspace[0].title, TITLE_1)
        self.assertEqual(workspace[0].owner, str(user.id))
        self.assertNotEqual(workspace[0].owner, str(fake_user_id))

    def test_post_create_workspace_without_title(self):
        """test_post_create_workspace_without_title

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        mock_data = {"owner": user.id}

        # Act
        response = RequestMock.do_request_post(
            workspace_rest_views.WorkspaceList.as_view(), user, data=mock_data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestWorkspaceReadAccess(IntegrationTransactionTestCase):
    """Test Workspace Read Access"""

    def test_get_workspace_with_read_access_return_http_200(self):
        """test_get_workspace_with_read_access_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_read_access, user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_workspace_with_read_access_own_workspace(self):
        """test_get_workspace_with_read_access_own_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_read_access, user
        )

        # Assert
        self.assertEqual(response.data[0]["title"], TITLE_1)

    def test_get_workspace_with_read_access_admin(self):
        """test_get_workspace_with_read_access_admin

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_super_user(username="user2")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_read_access, user2
        )

        # Assert
        self.assertEqual(response.data[0]["title"], TITLE_1)

    def test_get_workspace_with_read_access_other_workspace(self):
        """test_get_workspace_with_read_access_other_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_user_read_access_to_workspace(workspace, user2, user)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_read_access, user2
        )

        # Assert
        self.assertEqual(response.data[0]["title"], TITLE_1)

    def test_get_workspace_with_read_access_public_workspace(self):
        """test_get_workspace_with_read_access_public_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.set_workspace_public(workspace, user)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_read_access, user2
        )

        # Assert
        self.assertEqual(response.data[0]["title"], TITLE_1)


class TestWorkspaceWriteAccess(IntegrationTransactionTestCase):
    """Test Workspace Write Access"""

    def test_get_workspace_with_write_access_return_http_200(self):
        """test_get_workspace_with_write_access_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_write_access, user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_workspace_with_write_access_own_workspace(self):
        """test_get_workspace_with_write_access_own_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_write_access, user
        )

        # Assert
        self.assertEqual(response.data[0]["title"], TITLE_1)

    def test_get_workspace_with_write_access_admin(self):
        """test_get_workspace_with_write_access_admin

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_super_user(username="user2")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_write_access, user2
        )

        # Assert
        self.assertEqual(response.data[0]["title"], TITLE_1)

    def test_get_workspace_with_write_access_other_workspace(self):
        """test_get_workspace_with_write_access_other_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_user_write_access_to_workspace(
            workspace, user2, user
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_write_access, user2
        )

        # Assert
        self.assertEqual(response.data[0]["title"], TITLE_1)

    def test_get_workspace_with_write_access_public_workspace(self):
        """test_get_workspace_with_write_access_public_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.set_workspace_public(workspace, user)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_workspaces_with_write_access, user2
        )

        # Assert
        self.assertEqual(len(response.data), 0)


class TestWorkspaceIsPublic(IntegrationTransactionTestCase):
    """Test Workspace Is Public"""

    def test_is_workspace_public_return_http_200(self):
        """test_is_workspace_public_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.is_workspace_public,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_is_workspace_public_return_false(self):
        """test_is_workspace_public_return_false

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.is_workspace_public,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertFalse(response.data)

    def test_is_workspace_public_return_true(self):
        """test_is_workspace_public_return_true

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.set_workspace_public(workspace, user)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.is_workspace_public,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertTrue(response.data)

    def test_is_workspace_public_return_http_404(self):
        """test_is_workspace_public_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.is_workspace_public,
            user,
            param={"pk": FAKE_WORKSPACE_ID},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestWorkspaceSetPublic(IntegrationTransactionTestCase):
    """Test Workspace Set Public"""

    def test_set_workspace_public_return_http_200(self):
        """test_set_workspace_public_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_public,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_workspace_public_return_http_403(self):
        """test_set_workspace_public_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_public,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_set_workspace_public_return_http_404(self):
        """test_set_workspace_public_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_public,
            user,
            param={"pk": FAKE_WORKSPACE_ID},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_set_workspace_public_owner(self):
        """test_set_workspace_public_owner

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        self.assertFalse(workspace_api.is_workspace_public(workspace))

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_public,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        workspace = workspace_api.get_by_id(workspace.id)
        self.assertTrue(workspace_api.is_workspace_public(workspace))

    def test_set_workspace_public_admin_not_owner(self):
        """test_set_workspace_public_admin_not_owner

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_super_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        self.assertFalse(workspace_api.is_workspace_public(workspace))

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_public,
            user2,
            param={"pk": workspace.id},
        )

        # Assert
        workspace = workspace_api.get_by_id(workspace.id)
        self.assertTrue(workspace_api.is_workspace_public(workspace))

    def test_set_workspace_public_user_not_owner(self):
        """test_set_workspace_public_user_not_owner

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        self.assertFalse(workspace_api.is_workspace_public(workspace))

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_public,
            user2,
            param={"pk": workspace.id},
        )

        # Assert
        workspace = workspace_api.get_by_id(workspace.id)
        self.assertFalse(workspace_api.is_workspace_public(workspace))

    def test_set_workspace_public_user_not_owner_return_http_403(self):
        """test_set_workspace_public_user_not_owner_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        self.assertFalse(workspace_api.is_workspace_public(workspace))

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_public,
            user2,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestWorkspaceSetPrivate(IntegrationTransactionTestCase):
    """Test Workspace Set Private"""

    def test_set_workspace_private_return_http_200(self):
        """test_set_workspace_private_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_private,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_workspace_private_return_http_404(self):
        """test_set_workspace_private_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_private,
            user,
            param={"pk": FAKE_WORKSPACE_ID},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_set_workspace_private_owner(self):
        """test_set_workspace_private_owner

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.set_workspace_public(workspace, user)
        self.assertTrue(workspace_api.is_workspace_public(workspace))

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_private,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        workspace = workspace_api.get_by_id(workspace.id)
        self.assertFalse(workspace_api.is_workspace_public(workspace))

    def test_set_workspace_private_admin_not_owner(self):
        """test_set_workspace_private_admin_not_owner

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        user2 = UserFixtures().create_super_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.set_workspace_public(workspace, user)
        self.assertTrue(workspace_api.is_workspace_public(workspace))

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_private,
            user2,
            param={"pk": workspace.id},
        )

        # Assert
        workspace = workspace_api.get_by_id(workspace.id)
        self.assertFalse(workspace_api.is_workspace_public(workspace))

    def test_set_workspace_private_user_not_owner(self):
        """test_set_workspace_private_user_not_owner

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.set_workspace_public(workspace, user)
        self.assertTrue(workspace_api.is_workspace_public(workspace))

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_private,
            user2,
            param={"pk": workspace.id},
        )

        # Assert
        workspace = workspace_api.get_by_id(workspace.id)
        self.assertTrue(workspace_api.is_workspace_public(workspace))

    def test_set_workspace_private_user_not_owner_return_http_403(self):
        """test_set_workspace_private_user_not_owner_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        self.assertFalse(workspace_api.is_workspace_public(workspace))

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.set_workspace_private,
            user2,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestWorkspaceListUserCanRead(IntegrationTransactionTestCase):
    """Test Workspace List User Can read"""

    def test_get_list_user_can_read_workspace_return_http_200(self):
        """test_get_list_user_can_read_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_read_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_user_can_read_workspace_return_http_404(self):
        """test_get_list_user_can_read_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_read_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_list_user_can_read_workspace_return_http_403(self):
        """test_get_list_user_can_read_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_read_workspace,
            user2,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_user_can_read_workspace_owner(self):
        """test_get_list_user_can_read_workspace_owner

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_read_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_get_list_user_can_read_workspace_other_user(self):
        """test_get_list_user_can_read_workspace_other_user

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_user_read_access_to_workspace(workspace, user2, user)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_read_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], user2.id)
        self.assertEqual(response.data[0]["username"], user2.username)

    def test_get_list_user_can_read_workspace_public(self):
        """test_get_list_user_can_read_workspace_public

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.set_workspace_public(workspace, user)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_read_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 2)

    def test_get_list_user_can_read_workspace_other_user_admin(self):
        """test_get_list_user_can_read_workspace_other_user_admin

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        user3 = UserFixtures().create_super_user(username="user3")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_user_read_access_to_workspace(workspace, user2, user)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_read_workspace,
            user3,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], user2.id)
        self.assertEqual(response.data[0]["username"], user2.username)


class TestWorkspaceListUserCanWrite(IntegrationTransactionTestCase):
    """Test Workspace List User Can Write"""

    def test_get_list_user_can_write_workspace_return_http_200(self):
        """test_get_list_user_can_write_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_write_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_user_can_write_workspace_return_http_404(self):
        """test_get_list_user_can_write_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_write_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_list_user_can_write_workspace_return_http_403(self):
        """test_get_list_user_can_write_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_write_workspace,
            user2,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_user_can_write_workspace_owner(self):
        """test_get_list_user_can_write_workspace_owner

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_write_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_get_list_user_can_write_workspace_other_user(self):
        """test_get_list_user_can_write_workspace_other_user

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_user_write_access_to_workspace(
            workspace, user2, user
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_write_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], user2.id)
        self.assertEqual(response.data[0]["username"], user2.username)

    def test_get_list_user_can_write_workspace_public(self):
        """test_get_list_user_can_write_workspace_public

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.set_workspace_public(workspace, user)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_write_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_get_list_user_can_write_workspace_other_user_admin(self):
        """test_get_list_user_can_write_workspace_other_user_admin

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        user3 = UserFixtures().create_super_user(username="user3")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_user_write_access_to_workspace(
            workspace, user2, user
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_write_workspace,
            user3,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], user2.id)
        self.assertEqual(response.data[0]["username"], user2.username)


class TestWorkspaceListGroupCanRead(IntegrationTransactionTestCase):
    """Test Workspace List Group Can read"""

    def test_get_list_group_can_read_workspace_return_http_200(self):
        """test_get_list_group_can_read_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_read_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_group_can_read_workspace_return_http_404(self):
        """test_get_list_group_can_read_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_read_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_list_group_can_read_workspace_return_http_403(self):
        """test_get_list_group_can_read_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_read_workspace,
            user2,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_group_can_read_workspace_other_group(self):
        """test_get_list_group_can_read_workspace_other_group

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_group_read_access_to_workspace(
            workspace, group, user
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_read_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], group.id)
        self.assertEqual(response.data[0]["name"], group.name)

    def test_get_list_group_can_read_workspace_public(self):
        """test_get_list_group_can_read_workspace_public

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.set_workspace_public(workspace, user)
        GroupFixtures().create_group(name="group1")

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_read_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 3)

    def test_get_list_group_can_read_workspace_other_group_admin(self):
        """test_get_list_group_can_read_workspace_other_group_admin

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user3 = UserFixtures().create_super_user(username="user3")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        group = GroupFixtures().create_group(name="group1")
        workspace_api.add_group_read_access_to_workspace(
            workspace, group, user
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_read_workspace,
            user3,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], group.id)
        self.assertEqual(response.data[0]["name"], group.name)


class TestWorkspaceListGroupCanWrite(IntegrationTransactionTestCase):
    """Test Workspace List Group Can Write"""

    def test_get_list_group_can_write_workspace_return_http_200(self):
        """test_get_list_group_can_write_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_write_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_group_can_write_workspace_return_http_404(self):
        """test_get_list_group_can_write_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_write_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_list_group_can_write_workspace_return_http_403(self):
        """test_get_list_group_can_write_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_user_can_write_workspace,
            user2,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_group_can_write_workspace_other_group(self):
        """test_get_list_group_can_write_workspace_other_group

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_group_write_access_to_workspace(
            workspace, group, user
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_write_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], group.id)
        self.assertEqual(response.data[0]["name"], group.name)

    def test_get_list_group_can_write_workspace_public(self):
        """test_get_list_group_can_write_workspace_public

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        UserFixtures().add_publish_perm(user)
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.set_workspace_public(workspace, user)
        GroupFixtures().create_group(name="group1")

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_write_workspace,
            user,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_get_list_group_can_write_workspace_other_group_admin(self):
        """test_get_list_group_can_write_workspace_other_group_admin

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        user3 = UserFixtures().create_super_user(username="user3")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_group_write_access_to_workspace(
            workspace, group, user
        )

        # Act
        response = RequestMock.do_request_get(
            workspace_rest_views.get_list_group_can_write_workspace,
            user3,
            param={"pk": workspace.id},
        )

        # Assert
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], group.id)
        self.assertEqual(response.data[0]["name"], group.name)


class TestAddUserReadRightToWorkspace(IntegrationTransactionTestCase):
    """Test Add User Read Right To Workspace"""

    def test_add_user_read_right_to_workspace_return_http_200(self):
        """test_add_user_read_right_to_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_read_right_to_workspace,
            user,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_user_read_right_to_workspace_return_http_404(self):
        """test_add_user_read_right_to_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_read_right_to_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_user_read_right_to_workspace_return_http_403(self):
        """test_add_user_read_right_to_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_read_right_to_workspace,
            user2,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_user_read_right_to_workspace_(self):
        """test_add_user_read_right_to_workspace_

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        self.assertEqual(
            len(
                workspace_api.get_list_user_can_read_workspace(workspace, user)
            ),
            0,
        )

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.add_user_read_right_to_workspace,
            user,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(
            len(
                workspace_api.get_list_user_can_read_workspace(workspace, user)
            ),
            1,
        )


class TestAddUserWriteRightToWorkspace(IntegrationTransactionTestCase):
    """Test Add User Write Right To Workspace"""

    def test_add_user_write_right_to_workspace_return_http_200(self):
        """test_add_user_write_right_to_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_write_right_to_workspace,
            user,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_user_write_right_to_workspace_return_http_404(self):
        """test_add_user_write_right_to_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_write_right_to_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_user_write_right_to_workspace_return_http_403(self):
        """test_add_user_write_right_to_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_user_write_right_to_workspace,
            user2,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_user_write_right_to_workspace_(self):
        """test_add_user_write_right_to_workspace_

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        self.assertEqual(
            len(
                workspace_api.get_list_user_can_write_workspace(
                    workspace, user
                )
            ),
            0,
        )

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.add_user_write_right_to_workspace,
            user,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(
            len(
                workspace_api.get_list_user_can_write_workspace(
                    workspace, user
                )
            ),
            1,
        )


class TestAddGroupReadRightToWorkspace(IntegrationTransactionTestCase):
    """Test Add Group Read Right To Workspace"""

    def test_add_group_read_right_to_workspace_return_http_200(self):
        """test_add_group_read_right_to_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_read_right_to_workspace,
            user,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_group_read_right_to_workspace_return_http_404(self):
        """test_add_group_read_right_to_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_read_right_to_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_group_read_right_to_workspace_return_http_403(self):
        """test_add_group_read_right_to_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_read_right_to_workspace,
            user2,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_group_read_right_to_workspace_(self):
        """test_add_group_read_right_to_workspace_

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        self.assertEqual(
            len(
                workspace_api.get_list_group_can_read_workspace(
                    workspace, user
                )
            ),
            0,
        )

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.add_group_read_right_to_workspace,
            user,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(
            len(
                workspace_api.get_list_group_can_read_workspace(
                    workspace, user
                )
            ),
            1,
        )


class TestAddGroupWriteRightToWorkspace(IntegrationTransactionTestCase):
    """Test Add Group Write Right To Workspace"""

    def test_add_group_write_right_to_workspace_return_http_200(self):
        """test_add_group_write_right_to_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_write_right_to_workspace,
            user,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_group_write_right_to_workspace_return_http_404(self):
        """test_add_group_write_right_to_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_write_right_to_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_group_write_right_to_workspace_return_http_403(self):
        """test_add_group_write_right_to_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.add_group_write_right_to_workspace,
            user2,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_group_write_right_to_workspace(self):
        """test_add_group_write_right_to_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")

        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        self.assertEqual(
            len(
                workspace_api.get_list_group_can_write_workspace(
                    workspace, user
                )
            ),
            0,
        )

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.add_group_write_right_to_workspace,
            user,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(
            len(
                workspace_api.get_list_group_can_write_workspace(
                    workspace, user
                )
            ),
            1,
        )


class TestRemoveUserReadRightToWorkspace(IntegrationTransactionTestCase):
    """Test Remove User Read Right To Workspace"""

    def test_remove_user_read_right_to_workspace_return_http_200(self):
        """test_remove_user_read_right_to_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_read_right_to_workspace,
            user,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_user_read_right_to_workspace_return_http_404(self):
        """test_remove_user_read_right_to_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_read_right_to_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_user_read_right_to_workspace_return_http_403(self):
        """test_remove_user_read_right_to_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_read_right_to_workspace,
            user2,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_user_read_right_to_workspace(self):
        """
        test_remove_user_read_right_to_workspace
        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_user_read_access_to_workspace(workspace, user2, user)
        self.assertEqual(
            len(
                workspace_api.get_list_user_can_read_workspace(workspace, user)
            ),
            1,
        )

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.remove_user_read_right_to_workspace,
            user,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(
            len(
                workspace_api.get_list_user_can_read_workspace(workspace, user)
            ),
            0,
        )


class TestRemoveUserWriteRightToWorkspace(IntegrationTransactionTestCase):
    """Test Remove User Write Right To Workspace"""

    def test_remove_user_write_right_to_workspace_return_http_200(self):
        """test_remove_user_write_right_to_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_write_right_to_workspace,
            user,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_user_write_right_to_workspace_return_http_404(self):
        """test_remove_user_write_right_to_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_write_right_to_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_user_write_right_to_workspace_return_http_403(self):
        """test_remove_user_write_right_to_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_user_write_right_to_workspace,
            user2,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_user_write_right_to_workspace(self):
        """test_remove_user_write_right_to_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_user_write_access_to_workspace(
            workspace, user2, user
        )
        self.assertEqual(
            len(
                workspace_api.get_list_user_can_write_workspace(
                    workspace, user
                )
            ),
            1,
        )

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.remove_user_write_right_to_workspace,
            user,
            param={"pk": workspace.id, "user_id": user2.id},
        )

        # Assert
        self.assertEqual(
            len(
                workspace_api.get_list_user_can_write_workspace(
                    workspace, user
                )
            ),
            0,
        )


class TestRemoveGroupReadRightToWorkspace(IntegrationTransactionTestCase):
    """Test Remove Group Read Right To Workspace"""

    def test_remove_group_read_right_to_workspace_return_http_200(self):
        """test_remove_group_read_right_to_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_read_right_to_workspace,
            user,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_group_read_right_to_workspace_return_http_404(self):
        """test_remove_group_read_right_to_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_read_right_to_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_group_read_right_to_workspace_return_http_403(self):
        """test_remove_group_read_right_to_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_read_right_to_workspace,
            user2,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_group_read_right_to_workspace(self):
        """test_remove_group_read_right_to_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_group_read_access_to_workspace(
            workspace, group, user
        )
        self.assertEqual(
            len(
                workspace_api.get_list_group_can_read_workspace(
                    workspace, user
                )
            ),
            1,
        )

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.remove_group_read_right_to_workspace,
            user,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(
            len(
                workspace_api.get_list_group_can_read_workspace(
                    workspace, user
                )
            ),
            0,
        )


class TestRemoveGroupWriteRightToWorkspace(IntegrationTransactionTestCase):
    """Test Remove Group Write Right To Workspace"""

    def test_remove_group_write_right_to_workspace_return_http_200(self):
        """test_remove_group_write_right_to_workspace_return_http_200

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_write_right_to_workspace,
            user,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_group_write_right_to_workspace_return_http_404(self):
        """test_remove_group_write_right_to_workspace_return_http_404

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_write_right_to_workspace,
            user,
            param={"pk": FAKE_WORKSPACE_ID, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_group_write_right_to_workspace_return_http_403(self):
        """test_remove_group_write_right_to_workspace_return_http_403

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        user2 = UserFixtures().create_user(username="user2")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)

        # Act
        response = RequestMock.do_request_patch(
            workspace_rest_views.remove_group_write_right_to_workspace,
            user2,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_group_write_right_to_workspace(self):
        """test_remove_group_write_right_to_workspace

        Returns:

        """
        # Context
        user = UserFixtures().create_user(username="user1")
        group = GroupFixtures().create_group(name="group1")
        workspace = WorkspaceFixtures().create_workspace(user.id, TITLE_1)
        workspace_api.add_group_write_access_to_workspace(
            workspace, group, user
        )
        self.assertEqual(
            len(
                workspace_api.get_list_group_can_write_workspace(
                    workspace, user
                )
            ),
            1,
        )

        # Act
        RequestMock.do_request_patch(
            workspace_rest_views.remove_group_write_right_to_workspace,
            user,
            param={"pk": workspace.id, "group_id": group.id},
        )

        # Assert
        self.assertEqual(
            len(
                workspace_api.get_list_group_can_write_workspace(
                    workspace, user
                )
            ),
            0,
        )
