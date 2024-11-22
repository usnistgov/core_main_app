""" Unit tests for `ViewBlob` from `core_main_app.views.common.views` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.abstract_processing_module.models import (
    AbstractProcessingModule,
)
from core_main_app.views.common import views as common_views


class TestViewBlobGet(TestCase):
    """Unit test for `ViewBlob.get` method."""

    def setUp(self):
        """setUp"""
        self.view_assets = {
            "js": [
                {
                    "path": "core_main_app/user/js/blob/detail.js",
                }
            ],
            "css": [],
        }

        self.view = common_views.ViewBlob()
        self.mock_kwargs = {"request": MagicMock()}

    @patch.object(common_views, "blob_api")
    def test_blob_get_by_id_called(self, mock_blob_api):
        """test_blob_get_by_id_called"""
        self.view.get(**self.mock_kwargs)

        mock_blob_api.get_by_id.assert_called_with(
            self.mock_kwargs["request"].GET["id"],
            self.mock_kwargs["request"].user,
        )

    @patch.object(common_views, "blob_api")
    @patch("core_main_app.views.common.views.CommonView.common_render")
    def test_blob_get_by_id_dne_error_returns_404_error_page(
        self, mock_common_render, mock_blob_api
    ):
        """test_blob_get_by_id_dne_error_returns_404_error_page"""
        mock_blob_api.get_by_id.side_effect = DoesNotExist(
            "mock_dne_exception"
        )

        self.view.get(**self.mock_kwargs)

        mock_common_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_main_app/common/commons/error.html",
            context={
                "error": "Unable to access the requested file: Blob not found.",
                "status_code": 404,
                "page_title": "Error",
            },
        )

    @patch.object(common_views, "blob_api")
    @patch("core_main_app.views.common.views.CommonView.common_render")
    def test_blob_get_by_id_acl_error_returns_403_error_page(
        self, mock_common_render, mock_blob_api
    ):
        """test_blob_get_by_id_acl_error_returns_403_error_page"""

        mock_blob_api.get_by_id.side_effect = AccessControlError(
            "mock_acl_error"
        )

        self.view.get(**self.mock_kwargs)

        mock_common_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_main_app/common/commons/error.html",
            context={
                "error": "Unable to access the requested file: Access Forbidden.",
                "status_code": 403,
                "page_title": "Error",
            },
        )

    @patch.object(common_views, "blob_api")
    @patch("core_main_app.views.common.views.CommonView.common_render")
    def test_blob_get_by_id_exception_returns_400_error_page(
        self, mock_common_render, mock_blob_api
    ):
        """test_blob_get_by_id_exception_returns_400_error_page"""
        mock_exception = Exception("mock_exception")
        mock_blob_api.get_by_id.side_effect = mock_exception

        self.view.get(**self.mock_kwargs)

        mock_common_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_main_app/common/commons/error.html",
            context={
                "error": f"Unable to access the requested file: {str(mock_exception)}.",
                "status_code": 400,
                "page_title": "Error",
            },
        )

    @patch.object(common_views, "blob_api")
    @patch.object(common_views, "blob_module_api")
    def test_blob_module_get_all_by_blob_id_called(
        self, mock_blob_module_api, mock_blob_api
    ):
        """test_blob_module_get_all_by_blob_id_called"""

        self.view.get(**self.mock_kwargs)

        mock_blob_module_api.get_all_by_blob_id.assert_called_with(
            self.mock_kwargs["request"].GET["id"],
            self.mock_kwargs["request"].user,
            run_strategy=AbstractProcessingModule.RUN_ON_DEMAND,
        )

    @patch.object(common_views, "blob_api")
    @patch.object(common_views, "blob_module_api")
    @patch.object(common_views, "acl_api")
    @patch("core_main_app.views.common.views.CommonView.common_render")
    def test_blob_module_get_all_by_blob_id_acl_error_returns_empty_blob_module_list(
        self,
        mock_common_render,
        mock_acl_api,
        mock_blob_module_api,
        mock_blob_api,
    ):
        """test_blob_module_get_all_by_blob_id_acl_error_returns_empty_blob_module_list"""
        mock_blob = MagicMock()
        mock_blob_api.get_by_id.return_value = mock_blob
        mock_blob_module_api.get_all_by_blob_id.side_effect = (
            AccessControlError("mock_acl_error")
        )

        self.view.get(**self.mock_kwargs)

        mock_common_render.assert_called_with(
            self.mock_kwargs["request"],
            self.view.template,
            assets=self.view_assets,
            context={
                "blob": mock_blob,
                "can_write": True,
                "blob_modules": [],
                "page_title": "View File",
            },
        )

    @patch.object(common_views, "blob_api")
    @patch.object(common_views, "blob_module_api")
    @patch.object(common_views, "acl_api")
    def test_check_can_write_called(
        self, mock_acl_api, mock_blob_module_api, mock_blob_api
    ):
        """test_check_can_write_called"""
        mock_blob = MagicMock()
        mock_blob_api.get_by_id.return_value = mock_blob

        self.view.get(**self.mock_kwargs)

        mock_acl_api.check_can_write(
            mock_blob, self.mock_kwargs["request"].user
        )

    @patch.object(common_views, "blob_api")
    @patch.object(common_views, "blob_module_api")
    @patch.object(common_views, "acl_api")
    @patch("core_main_app.views.common.views.CommonView.common_render")
    def test_check_can_write_acl_error_returns_can_write_false(
        self,
        mock_common_render,
        mock_acl_api,
        mock_blob_module_api,
        mock_blob_api,
    ):
        """test_check_can_write_acl_error_returns_can_write_false"""
        mock_blob = MagicMock()
        mock_blob_api.get_by_id.return_value = mock_blob
        mock_blob_module_list = MagicMock()
        mock_blob_module_api.get_all_by_blob_id.return_value = (
            mock_blob_module_list
        )

        mock_acl_api.check_can_write.side_effect = AccessControlError(
            "mock_acl_error"
        )

        self.view.get(**self.mock_kwargs)

        mock_common_render.assert_called_with(
            self.mock_kwargs["request"],
            self.view.template,
            assets=self.view_assets,
            context={
                "blob": mock_blob,
                "can_write": False,
                "blob_modules": mock_blob_module_list,
                "page_title": "View File",
            },
        )

    @patch.object(common_views, "blob_api")
    @patch.object(common_views, "blob_module_api")
    @patch.object(common_views, "acl_api")
    @patch("core_main_app.views.common.views.CommonView.common_render")
    def test_common_render_called(
        self,
        mock_common_render,
        mock_acl_api,
        mock_blob_module_api,
        mock_blob_api,
    ):
        """test_success_returns_blob_view_page"""
        mock_blob = MagicMock()
        mock_blob_api.get_by_id.return_value = mock_blob
        mock_blob_module_list = MagicMock()
        mock_blob_module_api.get_all_by_blob_id.return_value = (
            mock_blob_module_list
        )

        self.view.get(**self.mock_kwargs)

        mock_common_render.assert_called_with(
            self.mock_kwargs["request"],
            self.view.template,
            assets=self.view_assets,
            context={
                "blob": mock_blob,
                "can_write": True,
                "blob_modules": mock_blob_module_list,
                "page_title": "View File",
            },
        )

    @patch.object(common_views, "blob_api")
    @patch.object(common_views, "blob_module_api")
    @patch.object(common_views, "acl_api")
    @patch("core_main_app.views.common.views.CommonView.common_render")
    def test_success_returns_blob_view_page(
        self,
        mock_common_render,
        mock_acl_api,
        mock_blob_module_api,
        mock_blob_api,
    ):
        """test_success_returns_blob_view_page"""
        mock_page = MagicMock()
        mock_common_render.return_value = mock_page

        self.assertEqual(self.view.get(**self.mock_kwargs), mock_page)
