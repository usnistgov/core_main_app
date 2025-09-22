""" Unit tests for `BlobProcessingModuleDynamicSerializerAPIView` view from
`core_main_app.rest.blob_processing_module.views` package
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from rest_framework import views as drf_views

from core_main_app.rest.blob_processing_module import (
    views as blob_processing_module_views,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestBlobProcessingModuleDynamicSerializerAPIViewGetPermissions(TestCase):
    """Unit test for `BlobProcessingModuleListView.get_permissions` method."""

    def setUp(self):
        """setUp"""
        self.mock_view = (
            blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView()
        )
        self.mock_request = MagicMock()

    @patch.object(drf_views.APIView, "get_permissions")
    def test_get_method_returns_default_permissions(
        self, mock_get_permissions
    ):
        """test_get_method_returns_default_permissions"""
        self.mock_request.method = "GET"
        self.mock_view.request = self.mock_request

        self.assertEqual(
            self.mock_view.get_permissions(), mock_get_permissions.return_value
        )

    @patch.object(blob_processing_module_views, "IsAdminUser")
    def test_post_method_returns_is_admin_permissions(
        self, mock_is_admin_user
    ):
        """test_post_method_returns_is_admin_permissions"""
        self.mock_request.method = "POST"
        self.mock_view.request = self.mock_request

        self.assertEqual(
            self.mock_view.get_permissions(), [mock_is_admin_user.return_value]
        )

    @patch.object(blob_processing_module_views, "IsAdminUser")
    def test_patch_method_returns_is_admin_permissions(
        self, mock_is_admin_user
    ):
        """test_patch_method_returns_is_admin_permissions"""
        self.mock_request.method = "PATCH"
        self.mock_view.request = self.mock_request

        self.assertEqual(
            self.mock_view.get_permissions(), [mock_is_admin_user.return_value]
        )

    @patch.object(blob_processing_module_views, "IsAdminUser")
    def test_delete_method_returns_is_admin_permissions(
        self, mock_is_admin_user
    ):
        """test_delete_method_returns_is_admin_permissions"""
        self.mock_request.method = "DELETE"
        self.mock_view.request = self.mock_request

        self.assertEqual(
            self.mock_view.get_permissions(), [mock_is_admin_user.return_value]
        )


class TestBlobProcessingModuleDynamicSerializerAPIViewGetSerializer(TestCase):
    """Unit test for `BlobProcessingModuleListView.get_serializer` method."""

    def setUp(self):
        """setUp"""
        self.non_staff_user = create_mock_user(1, is_staff=False)
        self.staff_user = create_mock_user(1, is_staff=True)

        self.mock_request = MagicMock()
        self.mock_request.user = self.staff_user

        self.mock_view = (
            blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView()
        )

    def test_write_serializer_returned_for_staff(self):
        """test_write_serializer_returned_for_staff"""
        self.assertEqual(
            self.mock_view.get_serializer(self.mock_request),
            blob_processing_module_views.BlobProcessingModuleWriteSerializer,
        )

    def test_read_serializer_returned_for_staff(self):
        """test_read_serializer_returned_for_staff"""
        self.mock_request.user = self.non_staff_user

        self.assertEqual(
            self.mock_view.get_serializer(self.mock_request),
            blob_processing_module_views.BlobProcessingModuleReadSerializer,
        )
