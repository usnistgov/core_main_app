""" Access control testing for Blob.
"""
import unittest
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from tests.components.blob.fixtures.fixtures import AccessControlBlobFixture
from tests.components.data.fixtures.fixtures import (
    AccessControlBlobWithMetadataFixture,
)

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.components.blob import api as blob_api
from core_main_app.components.blob.models import Blob
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user

fixture_blob = AccessControlBlobFixture()
fixture_blob_metadata = AccessControlBlobWithMetadataFixture()


class TestBlobGetById(IntegrationBaseTestCase):
    """TestBlobGetById"""

    fixture = fixture_blob

    def test_get_by_id_owner_with_read_access_returns_blob(self):
        """test_get_by_id_owner_with_read_access_returns_blob

        Returns:

        """
        blob_id = self.fixture.blob_collection[
            fixture_blob.USER_1_WORKSPACE_1
        ].id
        mock_user = _create_user("1")
        blob = blob_api.get_by_id(blob_id, mock_user)
        self.assertTrue(isinstance(blob, Blob))

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_by_id_user_without_read_access_raises_error(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_get_by_id_user_without_read_access_raises_error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        blob_id = self.fixture.blob_collection[
            fixture_blob.USER_1_WORKSPACE_1
        ].id
        get_all_workspaces_with_read_access_by_user.return_value = []
        mock_user = _create_user("2")
        with self.assertRaises(AccessControlError):
            blob_api.get_by_id(blob_id, mock_user)

    def test_get_by_id_owner_no_workspace_read_access_returns_blob(self):
        """test_get_by_id_owner_no_workspace_read_access_returns_blob

        Returns:

        """
        blob_id = self.fixture.blob_collection[
            fixture_blob.USER_1_NO_WORKSPACE
        ].id
        mock_user = _create_user("1")
        blob = blob_api.get_by_id(blob_id, mock_user)
        self.assertTrue(isinstance(blob, Blob))

    def test_get_by_id_not_owner_no_workspace_raises_error(self):
        """test_get_by_id_not_owner_no_workspace_raises_error

        Returns:

        """
        blob_id = self.fixture.blob_collection[
            fixture_blob.USER_1_NO_WORKSPACE
        ].id
        mock_user = _create_user("2")
        with self.assertRaises(AccessControlError):
            blob_api.get_by_id(blob_id, mock_user)


class TestBlobGetAll(IntegrationBaseTestCase):
    """TestBlobGetAll"""

    fixture = fixture_blob

    def test_get_all_as_superuser_returns_all_blob(self):
        """test_get_all_as_superuser_returns_all_blob

        Returns:

        """
        mock_user = _create_user("1", is_superuser=True)
        data_list = blob_api.get_all(mock_user)
        self.assertTrue(len(data_list) == len(self.fixture.blob_collection))

    def test_get_all_as_user_raises_error(self):
        """test_get_all_as_user_raises_error

        Returns:

        """
        mock_user = _create_user("1")
        with self.assertRaises(AccessControlError):
            blob_api.get_all(mock_user)


class TestBlobGetAllByUser(IntegrationBaseTestCase):
    """TestBlobGetAllByUser"""

    fixture = fixture_blob

    def test_get_all_by_user_returns_owned_blob(self):
        """test_get_all_by_user_returns_owned_blob

        Returns:

        """
        mock_user = _create_user("1")
        blob_list = blob_api.get_all_by_user(mock_user)
        self.assertTrue(len(blob_list) == 2)
        self.assertTrue(blob.id == "1" for blob in blob_list)

    def test_get_all_by_user_returns_no_blob_if_owns_zero(self):
        """test_get_all_by_user_returns_no_blob_if_owns_zero

        Returns:

        """
        mock_user = _create_user("3")
        blob_list = blob_api.get_all_by_user(mock_user)
        self.assertTrue(len(blob_list) == 0)

    def test_get_all_by_user_as_superuser_returns_own_blob(self):
        """test_get_all_by_user_as_superuser_returns_own_blob

        Returns:

        """
        mock_user = _create_user("1", is_superuser=True)
        blob_list = blob_api.get_all_by_user(mock_user)
        self.assertTrue(len(blob_list) == 2)
        self.assertTrue(blob.user_id == "1" for blob in blob_list)


class TestBlobGetAllByWorkspace(IntegrationBaseTestCase):
    """TestBlobGetAllByWorkspace"""

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
        """test_get_all_by_workspace_returns_owned_blob

        Args:
            get_all_workspaces_with_write_access_by_user:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user(self.fixture.USER_1_WORKSPACE_1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        get_all_workspaces_with_write_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        blob_list = blob_api.get_all_by_workspace(
            self.fixture.workspace_1, mock_user
        )
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
        """test_get_all_by_workspace_returns_no_blob_if_owns_zero

        Args:
            get_all_workspaces_with_write_access_by_user:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
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
        """test_get_all_by_workspace_as_superuser_returns_owned_blob

        Args:
            get_all_workspaces_with_write_access_by_user:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        get_all_workspaces_with_write_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        blob_list = blob_api.get_all_by_workspace(
            self.fixture.workspace_1, mock_user
        )
        self.assertTrue(blob.user_id == mock_user.id for blob in blob_list)


class TestBlobDelete(IntegrationBaseTestCase):
    """TestBlobDelete"""

    fixture = fixture_blob

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_blob_in_accessible_workspace_deletes_blob(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_delete_own_blob_in_accessible_workspace_deletes_blob

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_blob.workspace_1
        ]
        blob_api.delete(
            fixture_blob.blob_collection[fixture_blob.USER_1_WORKSPACE_1],
            mock_user,
        )

    # FIXME: test is not true. Deleting own data in workspace without write access raises ACL error.
    # (FIXME note also found in ACL code.)
    @unittest.skip("Test is not True.")
    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_blob_in_not_accessible_workspace_deletes_blob(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_delete_own_blob_in_not_accessible_workspace_deletes_blob

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = []
        blob_api.delete(
            fixture_blob.blob_collection[fixture_blob.USER_1_WORKSPACE_1],
            mock_user,
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_others_blob_in_accessible_workspace_deletes_blob(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_delete_others_blob_in_accessible_workspace_deletes_blob

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_blob.workspace_2
        ]
        blob_api.delete(
            fixture_blob.blob_collection[fixture_blob.USER_2_WORKSPACE_2],
            mock_user,
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_others_blob_not_accessible_workspace_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_delete_others_blob_not_accessible_workspace_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_blob.workspace_1
        ]
        with self.assertRaises(AccessControlError):
            blob_api.delete(
                fixture_blob.blob_collection[fixture_blob.USER_2_WORKSPACE_2],
                mock_user,
            )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_own_blob_not_in_workspace_deletes_blob(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_delete_own_blob_not_in_workspace_deletes_blob

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            blob_api.delete(
                fixture_blob.blob_collection[fixture_blob.USER_1_WORKSPACE_1],
                mock_user,
            )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_delete_others_blob_not_in_workspace_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_delete_others_blob_not_in_workspace_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        mock_user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            blob_api.delete(
                fixture_blob.blob_collection[fixture_blob.USER_2_NO_WORKSPACE],
                mock_user,
            )


class TestBlobChangeOwner(IntegrationBaseTestCase):
    """TestBlobChangeOwner"""

    fixture = fixture_blob

    def test_change_owner_from_owner_to_owner_ok(self):
        """test_change_owner_from_owner_to_owner_ok

        Returns:

        """
        mock_owner = _create_user("1")
        blob_api.change_owner(
            document=fixture_blob.blob_collection[
                fixture_blob.USER_1_NO_WORKSPACE
            ],
            new_user=mock_owner,
            user=mock_owner,
        )

    def test_change_owner_from_owner_to_user_ok(self):
        """test_change_owner_from_owner_to_user_ok

        Returns:

        """
        mock_owner = _create_user("1")
        mock_user = _create_user("2")
        blob_api.change_owner(
            document=fixture_blob.blob_collection[
                fixture_blob.USER_1_NO_WORKSPACE
            ],
            new_user=mock_user,
            user=mock_owner,
        )

    def test_change_owner_from_user_to_user_raises_exception(self):
        """test_change_owner_from_user_to_user_raises_exception

        Returns:

        """
        mock_owner = _create_user("1")
        mock_user = _create_user("2")
        with self.assertRaises(AccessControlError):
            blob_api.change_owner(
                document=fixture_blob.blob_collection[
                    fixture_blob.USER_1_NO_WORKSPACE
                ],
                new_user=mock_owner,
                user=mock_user,
            )

    def test_change_owner_as_superuser_ok(self):
        """test_change_owner_as_superuser_ok

        Returns:

        """
        mock_user = _create_user("2", is_superuser=True)
        blob_api.change_owner(
            document=fixture_blob.blob_collection[
                fixture_blob.USER_1_NO_WORKSPACE
            ],
            new_user=mock_user,
            user=mock_user,
        )


class TestBlobInsert(IntegrationBaseTestCase):
    """TestBlobInsert"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user = _create_user("1")
        self.superuser = _create_user("2", True)
        self.blob = Blob(
            filename="blob",
            user_id="1",
            blob=SimpleUploadedFile("blob.txt", b"blob"),
        )

    def test_insert_blob_as_anonymous_raises_error(self):
        """test_insert_blob_as_anonymous_raises_error

        Returns:

        """
        with self.assertRaises(AccessControlError):
            blob_api.insert(self.blob, self.anonymous_user)

    def test_insert_blob_as_user_creates_blob(
        self,
    ):
        """test_insert_blob_as_user_creates_blob

        Returns:

        """
        blob_api.insert(self.blob, self.user)

    def test_insert_blob_as_superuser_creates_blob(
        self,
    ):
        """test_insert_blob_as_superuser_creates_blob

        Returns:

        """
        blob_api.insert(self.blob, self.superuser)

    def test_edit_blob_as_user_raises_error(
        self,
    ):
        """test_edit_blob_as_user_raises_error

        Returns:

        """
        with self.assertRaises(exceptions.ApiError):
            blob_api.insert(
                fixture_blob.blob_collection[fixture_blob.USER_1_WORKSPACE_1],
                self.user,
            )

    def test_edit_blob_as_superuser_raises_error(
        self,
    ):
        """test_edit_blob_as_superuser_raises_error

        Returns:

        """
        with self.assertRaises(exceptions.ApiError):
            blob_api.insert(
                fixture_blob.blob_collection[fixture_blob.USER_1_NO_WORKSPACE],
                self.superuser,
            )


class TestBlobAssign(IntegrationBaseTestCase):
    """TestBlobAssign"""

    fixture = fixture_blob

    def test_assign_blob_as_anonymous_raises_error(self):
        """test_assign_blob_as_anonymous_raises_error

        Returns:

        """
        anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        with self.assertRaises(AccessControlError):
            blob_api.assign(
                self.fixture.blob_collection[fixture_blob.USER_1_NO_WORKSPACE],
                fixture_blob.workspace_1,
                anonymous_user,
            )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_assign_own_blob_to_accessible_workspace_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_assign_own_blob_to_accessible_workspace_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_blob.workspace_1
        ]
        blob_api.assign(
            fixture_blob.blob_collection[fixture_blob.USER_1_NO_WORKSPACE],
            fixture_blob.workspace_1,
            user,
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_assign_own_blob_to_inaccessible_workspace_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_assign_own_blob_to_inaccessible_workspace_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            blob_api.assign(
                fixture_blob.blob_collection[fixture_blob.USER_1_WORKSPACE_1],
                fixture_blob.workspace_2,
                user,
            )

    def test_assign_own_blob_with_no_workspace_to_none_ok(self):
        """test_assign_own_blob_with_no_workspace_to_none_ok

        Returns:

        """
        user = _create_user("1")
        blob_api.assign(
            fixture_blob.blob_collection[fixture_blob.USER_1_NO_WORKSPACE],
            None,
            user,
        )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_assign_others_blob_to_accessible_workspace_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_assign_others_blob_to_accessible_workspace_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = [
            fixture_blob.workspace_1
        ]
        with self.assertRaises(AccessControlError):
            blob_api.assign(
                fixture_blob.blob_collection[fixture_blob.USER_2_WORKSPACE_2],
                fixture_blob.workspace_1,
                user,
            )

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_assign_others_blob_to_inaccessible_workspace_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_assign_others_blob_to_inaccessible_workspace_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        user = _create_user("1")
        get_all_workspaces_with_write_access_by_user.return_value = []
        with self.assertRaises(AccessControlError):
            blob_api.assign(
                fixture_blob.blob_collection[fixture_blob.USER_2_WORKSPACE_2],
                fixture_blob.workspace_1,
                user,
            )

    def test_assign_blob_as_superuser_ok(
        self,
    ):
        """test_assign_blob_as_superuser_ok

        Returns:

        """
        user = _create_user("1", True)
        blob_api.assign(
            fixture_blob.blob_collection[fixture_blob.USER_2_NO_WORKSPACE],
            fixture_blob.workspace_1,
            user,
        )


class TestBlobMetadata(IntegrationBaseTestCase):
    """TestBlobMetadata"""

    fixture = fixture_blob_metadata

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_blob_metadata_as_owner_returns_metadata(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_blob_metadata_as_owner_returns_metadata

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_1
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        metadata = blob.metadata(mock_user)
        self.assertEqual(metadata, [self.fixture.data_1])

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_blob_metadata_private_metadata_as_other_user_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_blob_metadata_private_metadata_as_other_user_raises_acl_error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_1
        mock_user = create_mock_user(2)
        get_all_workspaces_with_read_access_by_user.return_value = []
        metadata = blob.metadata(mock_user)
        self.assertTrue(len(metadata) == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_blob_metadata_as_other_user_without_access_returns_nothing(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_blob_metadata_private_metadata_as_other_user_raises_acl_error

        Args:
            get_all_workspaces_with_read_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_2
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        metadata = blob.metadata(mock_user)
        self.assertTrue(len(metadata) == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_blob_metadata_other_user_metadata_in_workspace_with_access_returns_metadata(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_blob_metadata_other_user_metadata_in_workspace_with_access_returns_metadata

        Returns:

        """
        blob = self.fixture.blob_2
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        metadata = blob.metadata(mock_user)
        self.assertEqual(metadata, [self.fixture.data_2])

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_blob_metadata_other_user_metadata_in_workspace_without_access_does_not_return_metadata(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_blob_metadata_other_user_metadata_in_workspace_without_access_does_not_return_metadata

        Returns:

        """
        blob = self.fixture.blob_2
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        metadata = blob.metadata(mock_user)
        self.assertTrue(len(metadata) == 0)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_blob_metadata_other_user_metadata_returns_only_accessible_metadata(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_blob_metadata_other_user_metadata_returns_only_accessible_metadata

        Returns:

        """
        blob = self.fixture.blob_3
        mock_user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = [
            self.fixture.workspace_1
        ]
        metadata = blob.metadata(mock_user)
        self.assertEqual(metadata, [self.fixture.data_31])


class TestAddMetadata(IntegrationBaseTestCase):
    """TestAddMetadata"""

    fixture = fixture_blob_metadata

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_cannot_write_blob_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_cannot_write_blob_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_2
        data = self.fixture.data_4
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []

        with self.assertRaises(AccessControlError):
            blob_api.add_metadata(blob, data, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_cannot_write_data_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_cannot_write_data_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_2
        data = self.fixture.data_4
        mock_user = create_mock_user(2)
        get_all_workspaces_with_write_access_by_user.return_value = []

        with self.assertRaises(AccessControlError):
            blob_api.add_metadata(blob, data, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_own_blob_and_own_data_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_own_blob_and_own_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_1
        data = self.fixture.data_4
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []

        blob_api.add_metadata(blob, data, mock_user)
        self.assertEqual(data._blob, blob)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_own_blob_and_accessible_data_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_own_blob_and_accessible_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_1
        data = self.fixture.data_2
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []

        with self.assertRaises(AccessControlError):
            blob_api.add_metadata(blob, data, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_can_write_blob_and_own_data_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_can_write_blob_and_own_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_2
        data = self.fixture.data_4
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = [
            self.fixture.workspace_1
        ]

        blob_api.add_metadata(blob, data, mock_user)
        self.assertEqual(data._blob, blob)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_can_write_blob_and_can_write_data_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_can_write_blob_and_can_write_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_2
        data = self.fixture.data_4
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = [
            self.fixture.workspace_1
        ]

        blob_api.add_metadata(blob, data, mock_user)
        self.assertEqual(data._blob, blob)


class TestAddMetadataList(IntegrationBaseTestCase):
    """TestAddMetadataList"""

    fixture = fixture_blob_metadata

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_list_cannot_write_blob_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_list_cannot_write_blob_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_2
        data = self.fixture.data_4
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []

        with self.assertRaises(AccessControlError):
            blob_api.add_metadata_list(blob, [data], mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_list_cannot_write_data_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_list_cannot_write_data_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_2
        data = self.fixture.data_4
        mock_user = create_mock_user(2)
        get_all_workspaces_with_write_access_by_user.return_value = []

        with self.assertRaises(AccessControlError):
            blob_api.add_metadata_list(blob, [data], mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_list_own_blob_and_own_data_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_list_own_blob_and_own_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_1
        data = self.fixture.data_4
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []

        blob_api.add_metadata_list(blob, [data], mock_user)
        self.assertEqual(data._blob, blob)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_list_own_blob_and_accessible_data_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_list_own_blob_and_accessible_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_1
        data = self.fixture.data_2
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []

        with self.assertRaises(AccessControlError):
            blob_api.add_metadata_list(blob, [data], mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_list_can_write_blob_and_own_data_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_list_can_write_blob_and_own_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_2
        data = self.fixture.data_4
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = [
            self.fixture.workspace_1
        ]

        blob_api.add_metadata_list(blob, [data], mock_user)
        self.assertEqual(data._blob, blob)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_add_metadata_list_can_write_blob_and_can_write_data_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_add_metadata_list_can_write_blob_and_can_write_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_2
        data = self.fixture.data_4
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = [
            self.fixture.workspace_1
        ]

        blob_api.add_metadata_list(blob, [data], mock_user)
        self.assertEqual(data._blob, blob)


class TestRemoveMetadata(IntegrationBaseTestCase):
    """TestRemoveMetadata"""

    fixture = fixture_blob_metadata

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_remove_metadata_not_linked_to_blob_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_remove_metadata_not_linked_to_blob_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_1
        data = self.fixture.data_4
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []

        with self.assertRaises(Exception):
            blob_api.remove_metadata(blob, data, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_remove_metadata_cannot_write_blob_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_remove_metadata_cannot_write_blob_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_2
        data = self.fixture.data_2
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []

        with self.assertRaises(AccessControlError):
            blob_api.remove_metadata(blob, data, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_remove_metadata_cannot_write_data_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_remove_metadata_cannot_write_data_raises_error

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_2
        data = self.fixture.data_4
        mock_user = create_mock_user(2)
        get_all_workspaces_with_write_access_by_user.return_value = []

        with self.assertRaises(AccessControlError):
            blob_api.remove_metadata(blob, data, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_remove_metadata_own_blob_and_own_data_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_remove_metadata_own_blob_and_own_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_1
        data = self.fixture.data_1
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []

        blob_api.remove_metadata(blob, data, mock_user)
        self.assertEqual(blob._metadata.count(), 0)
        self.assertEqual(data._blob, None)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_remove_metadata_own_blob_and_accessible_data_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_remove_metadata_own_blob_and_accessible_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_1
        data = self.fixture.data_2
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = []

        with self.assertRaises(AccessControlError):
            blob_api.remove_metadata(blob, data, mock_user)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_remove_metadata_can_write_blob_and_can_write_data_ok(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_remove_metadata_can_write_blob_and_can_write_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_3
        data = self.fixture.data_31
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = [
            self.fixture.workspace_1
        ]

        blob_api.remove_metadata(blob, data, mock_user)
        self.assertEqual(blob._metadata.count(), 1)
        self.assertEqual(data._blob, None)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_write_access_by_user"
    )
    def test_remove_metadata_can_write_blob_and_cannot_write_data_raises_error(
        self, get_all_workspaces_with_write_access_by_user
    ):
        """test_remove_metadata_can_write_blob_and_can_write_data_ok

        Args:
            get_all_workspaces_with_write_access_by_user:

        Returns:

        """
        blob = self.fixture.blob_3
        data = self.fixture.data_32
        mock_user = create_mock_user(1)
        get_all_workspaces_with_write_access_by_user.return_value = [
            self.fixture.workspace_1
        ]

        with self.assertRaises(AccessControlError):
            blob_api.remove_metadata(blob, data, mock_user)


def _create_user(user_id, is_superuser=False):
    """_create_user

    Args:
        user_id:
        is_superuser:

    Returns:

    """
    return create_mock_user(user_id, is_superuser=is_superuser)
