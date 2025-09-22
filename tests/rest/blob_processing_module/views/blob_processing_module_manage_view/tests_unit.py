""" Unit tests for `BlobProcessingModuleManageView` view from
`core_main_app.rest.blob_processing_module.views` package
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from rest_framework import status
from rest_framework.exceptions import ValidationError

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.rest.blob_processing_module import (
    views as blob_processing_module_views,
)


class TestBlobProcessingModuleManageViewGet(TestCase):
    """Unit test for `BlobProcessingModuleManageView.get` method."""

    def setUp(self):
        """setUp"""
        self.mock_view = (
            blob_processing_module_views.BlobProcessingModuleManageView()
        )
        self.mock_kwargs = {
            "request": MagicMock(),
            "blob_processing_module_id": "mock_id",
        }

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_api_get_by_id_called(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_api_get_by_id_called"""
        self.mock_view.get(**self.mock_kwargs)

        mock_blob_processing_module_api.get_by_id.assert_called_with(
            self.mock_kwargs["blob_processing_module_id"],
            self.mock_kwargs["request"].user,
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_get_by_id_does_not_exist_returns_404(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_get_by_id_does_not_exist_returns_404"""
        mock_blob_processing_module_api.get_by_id.side_effect = DoesNotExist(
            "mock_does_not_exist"
        )

        result = self.mock_view.get(**self.mock_kwargs)

        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_get_by_id_acl_error_returns_403(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_get_all_acl_error_returns_403"""
        mock_blob_processing_module_api.get_by_id.side_effect = (
            AccessControlError("mock_acl_error")
        )

        result = self.mock_view.get(**self.mock_kwargs)

        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_get_by_id_exception_returns_500(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_get_by_id_exception_returns_500"""
        mock_blob_processing_module_api.get_by_id.side_effect = Exception(
            "mock_get_by_id_blob_processing_module_exception"
        )

        result = self.mock_view.get(**self.mock_kwargs)

        self.assertEqual(
            result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_blob_processing_module_get_serializer_called(
        self,
        mock_get_serializer,
        mock_blob_processing_module_api,
    ):
        """test_blob_processing_module_get_serializer_called"""
        mock_blob_processing_module = MagicMock()
        mock_blob_processing_module_api.get_by_id.return_value = (
            mock_blob_processing_module
        )

        self.mock_view.get(**self.mock_kwargs)

        mock_get_serializer.assert_called_with(self.mock_kwargs["request"])

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_blob_processing_module_serializer_instantiated(
        self,
        mock_get_serializer,
        mock_blob_processing_module_api,
    ):
        """test_blob_processing_module_serializer_instantiated"""
        mock_blob_processing_module = MagicMock()
        mock_blob_processing_module_api.get_by_id.return_value = (
            mock_blob_processing_module
        )

        mock_serializer = MagicMock()
        mock_get_serializer.return_value = mock_serializer

        self.mock_view.get(**self.mock_kwargs)

        mock_serializer.assert_called_with(
            mock_blob_processing_module,
            context={"request": self.mock_kwargs["request"]},
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_blob_processing_module_serializer_exception_returns_500(
        self,
        mock_get_serializer,
        mock_blob_processing_module_api,
    ):
        """test_blob_processing_module_serializer_exception_returns_500"""
        mock_blob_processing_module_api.get_by_id.return_value = MagicMock()

        mock_get_serializer.side_effect = Exception(
            "mock_serializer_exception"
        )

        result = self.mock_view.get(**self.mock_kwargs)

        self.assertEqual(
            result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_success_returns_200(
        self,
        mock_get_serializer,
        mock_blob_processing_module_api,
    ):
        """test_success_returns_200"""
        mock_blob_processing_module_api.get_by_id.return_value = MagicMock()

        mock_serializer = MagicMock()
        mock_get_serializer.return_value = mock_serializer

        result = self.mock_view.get(**self.mock_kwargs)

        self.assertEqual(result.status_code, status.HTTP_200_OK)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_success_returns_serializer_data(
        self,
        mock_get_serializer,
        mock_blob_processing_module_api,
    ):
        """test_success_returns_serializer_data"""
        mock_blob_processing_module_api.get_by_id.return_value = MagicMock()

        mock_serializer = MagicMock()
        mock_get_serializer.return_value = mock_serializer

        result = self.mock_view.get(**self.mock_kwargs)

        self.assertEqual(result.data, mock_serializer().data)


class TestBlobProcessingModuleManageViewPatch(TestCase):
    """Unit test for `BlobProcessingModuleManageView.patch` method."""

    def setUp(self):
        """setUp"""
        self.mock_view = (
            blob_processing_module_views.BlobProcessingModuleManageView()
        )
        self.mock_kwargs = {
            "request": MagicMock(),
            "blob_processing_module_id": "mock_id",
        }

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_api_get_by_id_called(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_api_get_by_id_called"""
        self.mock_view.patch(**self.mock_kwargs)

        mock_blob_processing_module_api.get_by_id.assert_called_with(
            self.mock_kwargs["blob_processing_module_id"],
            self.mock_kwargs["request"].user,
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_api_does_not_exist_returns_404(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_api_does_not_exist_returns_404"""
        mock_blob_processing_module_api.get_by_id.side_effect = DoesNotExist(
            "mock_does_not_exist"
        )

        result = self.mock_view.patch(**self.mock_kwargs)

        self.assertTrue(result.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_api_acl_error_returns_403(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_api_acl_error_returns_403"""
        mock_blob_processing_module_api.get_by_id.side_effect = (
            AccessControlError("mock_access_control_error")
        )

        result = self.mock_view.patch(**self.mock_kwargs)

        self.assertTrue(result.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_api_exception_returns_500(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_api_exception_returns_500"""
        mock_blob_processing_module_api.get_by_id.side_effect = Exception(
            "mock_exception"
        )

        result = self.mock_view.patch(**self.mock_kwargs)

        self.assertTrue(
            result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views, "BlobProcessingModuleWriteSerializer"
    )
    def test_blob_processing_module_serializer_called(
        self,
        mock_blob_processing_module_serializer,
        mock_blob_processing_module_api,
    ):
        """test_blob_processing_module_serializer_called"""
        mock_blob_processing_module = MagicMock()
        mock_blob_processing_module_api.get_by_id.return_value = (
            mock_blob_processing_module
        )

        self.mock_view.patch(**self.mock_kwargs)

        mock_blob_processing_module_serializer.assert_called_with(
            instance=mock_blob_processing_module,
            data=self.mock_kwargs["request"].data,
            partial=True,
            context={"request": self.mock_kwargs["request"]},
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views, "BlobProcessingModuleWriteSerializer"
    )
    def test_blob_processing_module_serializer_exception_returns_500(
        self,
        mock_blob_processing_module_serializer,
        mock_blob_processing_module_api,  # noqa
    ):
        """test_blob_processing_module_serializer_exception_returns_500"""
        mock_blob_processing_module_serializer.side_effect = Exception(
            "mock_exception"
        )

        result = self.mock_view.patch(**self.mock_kwargs)
        self.assertTrue(
            result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views, "BlobProcessingModuleWriteSerializer"
    )
    def test_blob_processing_module_serializer_is_valid_called(
        self,
        mock_blob_processing_module_serializer,
        mock_blob_processing_module_api,  # noqa
    ):
        """test_blob_processing_module_serializer_is_valid_called"""
        self.mock_view.patch(**self.mock_kwargs)

        mock_blob_processing_module_serializer().is_valid.assert_called_with(
            raise_exception=True
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views, "BlobProcessingModuleWriteSerializer"
    )
    def test_blob_processing_module_serializer_is_valid_error_returns_400(
        self,
        mock_blob_processing_module_serializer,
        mock_blob_processing_module_api,  # noqa
    ):
        """test_blob_processing_module_serializer_is_valid_error_returns_400"""
        mock_blob_processing_module_serializer.is_valid.side_effect = (
            ValidationError("mock_validation_error")
        )

        result = self.mock_view.patch(**self.mock_kwargs)
        self.assertTrue(result.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views, "BlobProcessingModuleWriteSerializer"
    )
    def test_blob_processing_module_serializer_is_valid_exception_returns_500(
        self,
        mock_blob_processing_module_serializer,
        mock_blob_processing_module_api,  # noqa
    ):
        """test_blob_processing_module_serializer_is_valid_exception_returns_500"""
        mock_blob_processing_module_serializer.is_valid.side_effect = (
            Exception("mock_exception")
        )

        result = self.mock_view.patch(**self.mock_kwargs)
        self.assertTrue(
            result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views, "BlobProcessingModuleWriteSerializer"
    )
    def test_blob_processing_module_serializer_save_called(
        self,
        mock_blob_processing_module_serializer,
        mock_blob_processing_module_api,  # noqa
    ):
        """test_blob_processing_module_serializer_save_called"""
        self.mock_view.patch(**self.mock_kwargs)

        mock_blob_processing_module_serializer().save.assert_called_with()

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views, "BlobProcessingModuleWriteSerializer"
    )
    def test_blob_processing_module_serializer_save_exception_returns_500(
        self,
        mock_blob_processing_module_serializer,
        mock_blob_processing_module_api,  # noqa
    ):
        """test_blob_processing_module_serializer_save_exception_returns_500"""
        mock_blob_processing_module_serializer.save.side_effect = Exception(
            "mock_exception"
        )

        result = self.mock_view.patch(**self.mock_kwargs)
        self.assertTrue(
            result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_success_returns_serializer_data(
        self,
        mock_blob_processing_module_serializer,
        mock_blob_processing_module_api,  # noqa
    ):
        """test_success_returns_serializer_data"""
        result = self.mock_view.patch(**self.mock_kwargs)
        self.assertTrue(
            result.data,
            mock_blob_processing_module_serializer().return_value.data,
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views, "BlobProcessingModuleWriteSerializer"
    )
    def test_success_returns_200(
        self,
        mock_blob_processing_module_serializer,  # noqa
        mock_blob_processing_module_api,  # noqa
    ):
        """test_success_returns_200"""
        result = self.mock_view.patch(**self.mock_kwargs)
        self.assertTrue(result.status_code, status.HTTP_200_OK)


class TestBlobProcessingModuleManageViewDelete(TestCase):
    """Unit test for `BlobProcessingModuleManageView.delete` method."""

    def setUp(self):
        """setUp"""
        self.mock_view = (
            blob_processing_module_views.BlobProcessingModuleManageView()
        )
        self.mock_kwargs = {
            "request": MagicMock(),
            "blob_processing_module_id": "mock_id",
        }

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_api_delete_called(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_api_delete_called"""
        self.mock_view.delete(**self.mock_kwargs)

        mock_blob_processing_module_api.delete.assert_called_with(
            self.mock_kwargs["blob_processing_module_id"],
            self.mock_kwargs["request"].user,
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_api_does_not_exist_returns_404(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_api_does_not_exist_returns_404"""
        mock_blob_processing_module_api.delete.side_effect = DoesNotExist(
            "mock_does_not_exist"
        )

        result = self.mock_view.delete(**self.mock_kwargs)

        self.assertTrue(result.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_api_acl_error_returns_403(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_api_acl_error_returns_403"""
        mock_blob_processing_module_api.delete.side_effect = (
            AccessControlError("mock_access_control_error")
        )

        result = self.mock_view.delete(**self.mock_kwargs)

        self.assertTrue(result.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_api_exception_returns_500(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_api_exception_returns_500"""
        mock_blob_processing_module_api.delete.side_effect = Exception(
            "mock_exception"
        )

        result = self.mock_view.delete(**self.mock_kwargs)

        self.assertTrue(
            result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_success_returns_204(
        self,
        mock_blob_processing_module_api,  # noqa
    ):
        """test_success_returns_200"""
        result = self.mock_view.delete(**self.mock_kwargs)
        self.assertTrue(result.status_code, status.HTTP_204_NO_CONTENT)
