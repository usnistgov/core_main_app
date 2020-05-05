""" Access control testing for Blob.
"""
import unittest

from mock.mock import patch

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.blob import api as blob_api
from core_main_app.components.blob.models import Blob
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.components.blob.fixtures.fixtures import AccessControlBlobFixture

fixture_blob = AccessControlBlobFixture()


class TestBlobGetById(MongoIntegrationBaseTestCase):

    fixture = fixture_blob

    def test_get_by_id_owner_with_read_access_returns_blob(self):
        blob_id = self.fixture.blob_collection[fixture_blob.USER_1_WORKSPACE_1].id
        mock_user = _create_user("1")
        blob = blob_api.get_by_id(blob_id, mock_user)
        self.assertTrue(isinstance(blob, Blob))

    def test_get_by_id_owner_without_read_access_returns_blob(self):
        blob_id = self.fixture.blob_collection[fixture_blob.USER_1_WORKSPACE_1].id
        mock_user = _create_user("1")
        with self.assertRaises(AccessControlError):
            blob_api.get_by_id(blob_id, mock_user)

    def test_get_by_id_owner_without_read_access_returns_blob(self):
        blob_id = self.fixture.blob_collection[fixture_blob.USER_1_WORKSPACE_1].id
        mock_user = _create_user("1")
        blob = blob_api.get_by_id(blob_id, mock_user)
        self.assertTrue(isinstance(blob, Blob))

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_by_id_user_without_read_access_raises_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        blob_id = self.fixture.blob_collection[fixture_blob.USER_1_WORKSPACE_1].id
        get_all_workspaces_with_read_access_by_user.return_value = []
        mock_user = _create_user("2")
        with self.assertRaises(AccessControlError):
            blob_api.get_by_id(blob_id, mock_user)

    def test_get_by_id_owner_no_workspace_read_access_returns_blob(self):
        blob_id = self.fixture.blob_collection[fixture_blob.USER_1_NO_WORKSPACE].id
        mock_user = _create_user("1")
        blob = blob_api.get_by_id(blob_id, mock_user)
        self.assertTrue(isinstance(blob, Blob))

    def test_get_by_id_not_owner_no_workspace_raises_error(self):
        blob_id = self.fixture.blob_collection[fixture_blob.USER_1_NO_WORKSPACE].id
        mock_user = _create_user("2")
        with self.assertRaises(AccessControlError):
            blob_api.get_by_id(blob_id, mock_user)


class TestBlobGetAll(MongoIntegrationBaseTestCase):

    fixture = fixture_blob

    def test_get_all_as_superuser_returns_all_blob(self):
        mock_user = _create_user("1", is_superuser=True)
        data_list = blob_api.get_all(mock_user)
        self.assertTrue(len(data_list) == len(self.fixture.blob_collection))

    def test_get_all_as_user_raises_error(self):
        mock_user = _create_user("1")
        with self.assertRaises(AccessControlError):
            blob_api.get_all(mock_user)


class TestBlobGetAllByUser(MongoIntegrationBaseTestCase):

    fixture = fixture_blob

    def test_get_all_by_user_returns_owned_blob(self):
        mock_user = _create_user("1")
        blob_list = blob_api.get_all_by_user(mock_user)
        self.assertTrue(len(blob_list) == 2)
        self.assertTrue(blob.id == "1" for blob in blob_list)

    def test_get_all_by_user_returns_no_blob_if_owns_zero(self):
        mock_user = _create_user("3")
        blob_list = blob_api.get_all_by_user(mock_user)
        self.assertTrue(len(blob_list) == 0)

    def test_get_all_by_user_as_superuser_returns_own_blob(self):
        mock_user = _create_user("1", is_superuser=True)
        blob_list = blob_api.get_all_by_user(mock_user)
        self.assertTrue(len(blob_list) == 2)
        self.assertTrue(blob.user_id == "1" for blob in blob_list)


class TestBlobGetAllByWorkspace(MongoIntegrationBaseTestCase):

    fixture = fixture_blob

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_by_workspace_returns_owned_blob(
        self,
        get_all_workspaces_with_write_access_by_user,
        get_all_workspaces_with_read_access_by_user,
    ):
        mock_user = _create_user(self.fixture.USER_1_WORKSPACE_1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        get_all_workspaces_with_write_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        blob_list = blob_api.get_all_by_workspace(self.fixture.workspace_1, mock_user)
        self.assertTrue(blob.user_id == mock_user.id for blob in blob_list)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_by_workspace_returns_no_blob_if_owns_zero(
        self,
        get_all_workspaces_with_write_access_by_user,
        get_all_workspaces_with_read_access_by_user,
    ):
        mock_user = _create_user("7")
        get_all_workspaces_with_write_access_by_user.return_value = []
        get_all_workspaces_with_read_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            blob_api.get_all_by_workspace(self.fixture.workspace_1, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_all_by_workspace_as_superuser_returns_owned_blob(
        self,
        get_all_workspaces_with_write_access_by_user,
        get_all_workspaces_with_read_access_by_user,
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        get_all_workspaces_with_write_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        blob_list = blob_api.get_all_by_workspace(self.fixture.workspace_1, mock_user)
        self.assertTrue(blob.user_id == mock_user.id for blob in blob_list)


class TestBlobDelete(MongoIntegrationBaseTestCase):

    fixture = fixture_blob

    @unittest.skip("GridFS not supported by mongomock")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_blob_in_accessible_workspace_deletes_blob(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_blob.workspace_1
        ]
        blob_api.delete(
            fixture_blob.blob_collection[fixture_blob.USER_1_WORKSPACE_1], mock_user
        )

    @unittest.skip("GridFS not supported by mongomock")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_blob_in_not_accessible_workspace_deletes_blob(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = []
        blob_api.delete(
            fixture_blob.blob_collection[fixture_blob.USER_1_WORKSPACE_1], mock_user
        )

    @unittest.skip("GridFS not supported by mongomock")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_others_blob_in_accessible_workspace_deletes_blob(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_blob.workspace_2
        ]
        blob_api.delete(
            fixture_blob.blob_collection[fixture_blob.USER_2_WORKSPACE_2], mock_user
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_others_blob_not_accessible_workspace_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_blob.workspace_1
        ]
        with self.assertRaises(AccessControlError):
            blob_api.delete(
                fixture_blob.blob_collection[fixture_blob.USER_2_WORKSPACE_2], mock_user
            )

    @unittest.skip("GridFS not supported by mongomock")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_blob_not_in_workspace_deletes_blob(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            blob_api.delete(
                fixture_blob.blob_collection[fixture_blob.USER_1_WORKSPACE_1], mock_user
            )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_others_blob_not_in_workspace_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            blob_api.delete(
                fixture_blob.blob_collection[fixture_blob.USER_2_NO_WORKSPACE],
                mock_user,
            )


class TestBlobChangeOwner(MongoIntegrationBaseTestCase):

    fixture = fixture_blob

    def test_change_owner_from_owner_to_owner_ok(self):
        mock_owner = _create_user("1")
        blob_api.change_owner(
            document=fixture_blob.blob_collection[fixture_blob.USER_1_NO_WORKSPACE],
            new_user=mock_owner,
            user=mock_owner,
        )

    def test_change_owner_from_owner_to_user_ok(self):
        mock_owner = _create_user("1")
        mock_user = _create_user("2")
        blob_api.change_owner(
            document=fixture_blob.blob_collection[fixture_blob.USER_1_NO_WORKSPACE],
            new_user=mock_user,
            user=mock_owner,
        )

    def test_change_owner_from_user_to_user_raises_exception(self):
        mock_owner = _create_user("1")
        mock_user = _create_user("2")
        with self.assertRaises(AccessControlError):
            blob_api.change_owner(
                document=fixture_blob.blob_collection[fixture_blob.USER_1_NO_WORKSPACE],
                new_user=mock_owner,
                user=mock_user,
            )

    def test_change_owner_as_superuser_ok(self):
        mock_user = _create_user("2", is_superuser=True)
        blob_api.change_owner(
            document=fixture_blob.blob_collection[fixture_blob.USER_1_NO_WORKSPACE],
            new_user=mock_user,
            user=mock_user,
        )


def _create_user(user_id, is_superuser=False):
    return create_mock_user(user_id, is_superuser=is_superuser)
