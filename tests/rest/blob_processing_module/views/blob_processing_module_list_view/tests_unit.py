""" Unit tests for `BlobProcessingModuleListView` view from
`core_main_app.rest.blob_processing_module.views` package
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from rest_framework import status
from rest_framework.exceptions import ValidationError

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.rest.blob_processing_module import (
    views as blob_processing_module_views,
)


class TestBlobProcessingModuleListViewGet(TestCase):
    """Unit test for `BlobProcessingModuleListView.get` method."""

    def setUp(self):
        """setUp"""
        self.mock_view = (
            blob_processing_module_views.BlobProcessingModuleListView()
        )
        self.mock_kwargs = {"request": MagicMock()}

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_get_all_called(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_get_all_called"""
        self.mock_view.get(**self.mock_kwargs)

        mock_blob_processing_module_api.get_all.assert_called_with(
            self.mock_kwargs["request"].user
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_get_all_acl_error_returns_403(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_get_all_acl_error_returns_403"""
        mock_blob_processing_module_api.get_all.side_effect = (
            AccessControlError("mock_acl_error")
        )

        result = self.mock_view.get(**self.mock_kwargs)

        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    def test_blob_processing_module_get_all_exception_returns_500(
        self, mock_blob_processing_module_api
    ):
        """test_blob_processing_module_get_all_exception_returns_500"""
        mock_blob_processing_module_api.get_all.side_effect = Exception(
            "mock_get_all_blob_processing_module_exception"
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
        mock_blob_processing_module_list = MagicMock()
        mock_blob_processing_module_api.get_all.return_value = (
            mock_blob_processing_module_list
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
        mock_blob_processing_module_list = MagicMock()
        mock_blob_processing_module_api.get_all.return_value = (
            mock_blob_processing_module_list
        )

        mock_serializer = MagicMock()
        mock_get_serializer.return_value = mock_serializer

        self.mock_view.get(**self.mock_kwargs)

        mock_serializer.assert_called_with(
            mock_blob_processing_module_list,
            many=True,
            context={"request": self.mock_kwargs["request"]},
        )

    @patch.object(blob_processing_module_views, "blob_processing_module_api")
    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_blob_processing_module_get_serializer_exception_returns_500(
        self,
        mock_get_serializer,
        mock_blob_processing_module_api,
    ):
        """test_blob_processing_module_get_serializer_exception_returns_500"""
        mock_blob_processing_module_api.get_all.return_value = MagicMock()

        mock_get_serializer.side_effect = Exception(
            "mock_get_serializer_exception"
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
        mock_blob_processing_module_api.get_all.return_value = MagicMock()

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
        mock_blob_processing_module_api.get_all.return_value = MagicMock()

        mock_serializer = MagicMock()
        mock_get_serializer.return_value = mock_serializer

        result = self.mock_view.get(**self.mock_kwargs)

        self.assertEqual(result.data, mock_serializer().data)


class TestBlobProcessingModuleListViewPost(TestCase):
    """Unit test for `BlobProcessingModuleListView.post` method."""

    def setUp(self):
        """setUp"""
        self.mock_view = (
            blob_processing_module_views.BlobProcessingModuleListView()
        )
        self.mock_kwargs = {"request": MagicMock()}

    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_blob_processing_module_get_serializer_called(
        self, mock_get_serializer
    ):
        """test_blob_processing_module_get_serializer_called"""
        self.mock_view.post(**self.mock_kwargs)

        mock_get_serializer.assert_called_with(self.mock_kwargs["request"])

    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_blob_processing_module_serializer_instantiated(
        self, mock_get_serializer
    ):
        """test_blob_processing_module_serializer_instantiated"""
        mock_serializer = MagicMock()
        mock_get_serializer.return_value = mock_serializer

        self.mock_view.post(**self.mock_kwargs)

        mock_serializer.assert_called_with(
            data=self.mock_kwargs["request"].data,
            context={"request": self.mock_kwargs["request"]},
        )

    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_serializer_is_valid_called(self, mock_get_serializer):
        """test_serializer_is_valid_called"""
        mock_serializer = MagicMock()
        mock_get_serializer.return_value = mock_serializer

        self.mock_view.post(**self.mock_kwargs)

        mock_serializer().is_valid.assert_called_with(raise_exception=True)

    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_serializer_save_called(self, mock_get_serializer):
        """test_serializer_save_called"""
        mock_serializer = MagicMock()
        mock_get_serializer.return_value = mock_serializer

        self.mock_view.post(**self.mock_kwargs)

        mock_serializer().save.assert_called_with()

    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_no_error_returns_201_response(self, mock_get_serializer):  # noqa
        """test_no_error_returns_201_response"""
        result = self.mock_view.post(**self.mock_kwargs)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_no_error_returns_serializer_data(self, mock_get_serializer):
        """test_no_error_returns_201_response"""
        mock_serializer = MagicMock()
        mock_get_serializer.return_value = mock_serializer
        result = self.mock_view.post(**self.mock_kwargs)

        self.assertEqual(result.data, mock_serializer().data)

    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_validation_error_returns_400_response(self, mock_get_serializer):
        """test_validation_error_returns_400_response"""
        mock_serializer = MagicMock()
        mock_get_serializer.return_value = mock_serializer

        mock_serializer().is_valid.side_effect = ValidationError(
            "mock_validation_error"
        )

        result = self.mock_view.post(**self.mock_kwargs)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(
        blob_processing_module_views.BlobProcessingModuleDynamicSerializerAPIView,
        "get_serializer",
    )
    def test_exception_returns_500_response(self, mock_get_serializer):
        """test_exception_returns_500_response"""
        mock_get_serializer.side_effect = Exception("mock_exception")

        result = self.mock_view.post(**self.mock_kwargs)
        self.assertEqual(
            result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
