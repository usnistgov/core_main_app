""" Test units
"""

from os.path import join, dirname, realpath
from unittest.case import TestCase
from unittest.mock import patch, MagicMock, Mock

from django.contrib import admin
from django.urls import reverse, resolve
from rest_framework import status

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.xsl_transformation import (
    api as xsl_transformation_api,
)
from core_main_app.components.xsl_transformation.admin_site import (
    CustomXslTransformationAdmin,
)
from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from xml_utils.html_tree.parser import html_diff as htmldiff


class TestXslTransformationGet(TestCase):
    """TestXslTransformationGet"""

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transformation_get_return_xsl_transformation(
        self, mock_get_by_name
    ):
        """test xsl transformation get return xsl transformation

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_xslt = _create_mock_xsl_transformation(
            name="xslt_name", filename="xslt_filename", content="xslt_content"
        )

        mock_get_by_name.return_value = mock_xslt

        # Act
        result = xsl_transformation_api.get_by_name(mock_xslt.name)

        # Assert
        self.assertIsInstance(result, XslTransformation)

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transformation_get_raises_exception_if_object_does_not_exists(
        self, mock_get_by_name
    ):
        """test xsl transformation get raises exception if object does not exists

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_bad_name = "bad_xslt_name"
        mock_get_by_name.side_effect = exceptions.DoesNotExist("error")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            xsl_transformation_api.get_by_name(mock_bad_name)


class TestXslTransformationGetById(TestCase):
    """TestXslTransformationGetById"""

    @patch.object(XslTransformation, "get_by_id")
    def test_xsl_transformation_get_by_id_raises_api_error_if_does_not_exisst(
        self, mock_get
    ):
        """test xsl transformation get by id raises api error if does not exisst

        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            xsl_transformation_api.get_by_id(1)

    @patch.object(XslTransformation, "get_by_id")
    def test_xsl_transformation_get_by_id_returns_xsl_transformation(
        self, mock_get
    ):
        """test xsl transformation get by id returns xsl transformation

        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_data = _create_mock_xsl_transformation(
            name="xslt_name_1",
            filename="xslt_filename_1",
            content="xslt_content_1",
        )
        mock_get.return_value = mock_data

        # Act
        result = xsl_transformation_api.get_by_id(1)

        # Assert
        self.assertIsInstance(result, XslTransformation)


class TestXslTransformationGetAll(TestCase):
    """TestXslTransformationGetAll"""

    @patch.object(XslTransformation, "get_all")
    def test_xsl_transformation_get_all_contains_only_xsl_transformation(
        self, mock_get_all
    ):
        """test xsl transformation get all contains only xsl transformation

        Args:
            mock_get_all:

        Returns:

        """
        # Arrange
        mock_xslt_1 = _create_mock_xsl_transformation(
            name="xslt_name_1",
            filename="xslt_filename_1",
            content="xslt_content_1",
        )

        mock_xslt_2 = _create_mock_xsl_transformation(
            name="xslt_name_2",
            filename="xslt_filename_2",
            content="xslt_content_2",
        )

        mock_get_all.return_value = [mock_xslt_1, mock_xslt_2]

        # Act
        result = xsl_transformation_api.get_all()

        # Assert
        self.assertTrue(
            all(isinstance(item, XslTransformation) for item in result)
        )


class TestXslTransformationUpsert(TestCase):
    """TestXslTransformationUpsert"""

    @patch.object(XslTransformation, "save")
    def test_xsl_transformation_upsert_return_xsl_transformation(
        self, mock_save
    ):
        """test xsl transformation upsert return xsl transformation

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        mock_name = "xslt_name"
        mock_filename = "xslt_filename"
        mock_content = (
            "<xsl:stylesheet xmlns:xsl='http://www.w3.org/1999/XSL/Transform' version='1.0'> "
            "<xsl:output method='html' indent='yes' encoding='UTF-8' />"
            "<root></root></xsl:stylesheet>"
        )

        mock_xslt = _create_xsl_transformation(
            name=mock_name, filename=mock_filename, content=mock_content
        )

        mock_save.return_value = mock_xslt

        # Act
        result = xsl_transformation_api.upsert(mock_xslt)

        # Assert
        self.assertIsInstance(result, XslTransformation)

    @patch.object(XslTransformation, "save")
    def test_xsl_transformation_upsert_raises_exception_if_not_well_formatted(
        self, mock_save
    ):
        """test xsl transformation upsert raises exception if not well formatted

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        mock_name = "xslt_name"
        mock_filename = "xslt_filename"
        mock_content = "bad_content"

        mock_xslt = _create_xsl_transformation(
            name=mock_name, filename=mock_filename, content=mock_content
        )

        mock_save.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.upsert(mock_xslt)

    @patch.object(XslTransformation, "save")
    def test_xsl_transformation_upsert_raises_exception_if_bad_namespace(
        self, mock_save
    ):
        """test xsl transformation upsert raises exception if bad namespace

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        mock_name = "xslt_name"
        mock_filename = "xslt_filename"
        mock_content = "<root></root>"

        mock_xslt = _create_xsl_transformation(
            name=mock_name, filename=mock_filename, content=mock_content
        )

        mock_save.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.upsert(mock_xslt)


class TestXslTransformationAdminViews(TestCase):
    """Test Custom XslTransformation Admin Views"""

    def setUp(self):
        """setUp"""
        self.anonymous = create_mock_user(
            user_id=None, is_staff=False, is_superuser=False
        )
        self.user = create_mock_user(
            user_id="1", is_staff=False, is_superuser=False
        )
        self.staff_user = create_mock_user(
            user_id="2", is_staff=True, is_superuser=False
        )
        self.superuser = create_mock_user(
            user_id="3", is_staff=True, is_superuser=True
        )

    @patch("core_main_app.components.xsl_transformation.admin_site.diff_files")
    def test_anonymous_cannot_access_diff_file_view(self, mock_diff_files):
        """test_anonymous_cannot_access_diff_file_view"""
        xslt_id = 1
        index = 0
        url = reverse("admin:diff_file_xslt", args=[xslt_id, index])
        view = resolve(url).func
        response = RequestMock.do_request_get(view, user=self.anonymous)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertFalse(mock_diff_files.called)

    @patch("core_main_app.components.xsl_transformation.admin_site.diff_files")
    def test_user_cannot_access_diff_file_view(self, mock_diff_files):
        """test_user_cannot_access_diff_file_view"""
        xslt_id = 1
        index = 0
        url = reverse("admin:diff_file_xslt", args=[xslt_id, index])
        view = resolve(url).func
        response = RequestMock.do_request_get(view, user=self.user)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertFalse(mock_diff_files.called)

    @patch("core_main_app.components.xsl_transformation.admin_site.diff_files")
    def test_staff_user_cannot_access_diff_file_view(self, mock_diff_files):
        """test_staff_user_cannot_access_diff_file_view"""
        xslt_id = 1
        index = 0
        url = reverse("admin:diff_file_xslt", args=[xslt_id, index])
        view = resolve(url).func
        response = RequestMock.do_request_get(
            view,
            param={"object_id": xslt_id, "index": index},
            user=self.staff_user,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(mock_diff_files.called)

    @patch("core_main_app.components.xsl_transformation.admin_site.diff_files")
    @patch("core_main_app.components.xsl_transformation.api.get_by_id")
    def test_superuser_can_access_diff_file_view(
        self, mock_get_xslt_by_id, mock_diff_files
    ):
        """test_superuser_can_access_diff_file_view"""
        mock_get_xslt_by_id.return_value = MagicMock()
        xslt_id = 1
        index = 0
        url = reverse("admin:diff_file_xslt", args=[xslt_id, index])
        view = resolve(url).func
        response = RequestMock.do_request_get(
            view,
            param={"object_id": xslt_id, "index": index},
            user=self.superuser,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_diff_files.called)

    @patch(
        "core_main_app.components.xsl_transformation.admin_site.delete_previous_file"
    )
    def test_anonymous_cannot_access_delete_file_view(
        self, mock_delete_previous_file
    ):
        """test_anonymous_cannot_access_delete_file_view"""
        xslt_id = 1
        index = 0
        url = reverse("admin:delete_file_xslt", args=[xslt_id, index])
        view = resolve(url).func
        response = RequestMock.do_request_get(
            view,
            param={"object_id": xslt_id, "index": index},
            user=self.anonymous,
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertFalse(mock_delete_previous_file.called)

    @patch(
        "core_main_app.components.xsl_transformation.admin_site.delete_previous_file"
    )
    def test_user_cannot_access_delete_file_view(
        self, mock_delete_previous_file
    ):
        """test_user_cannot_access_delete_file_view"""
        xslt_id = 1
        index = 0
        url = reverse("admin:delete_file_xslt", args=[xslt_id, index])
        view = resolve(url).func
        response = RequestMock.do_request_get(
            view,
            param={"object_id": xslt_id, "index": index},
            user=self.user,
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertFalse(mock_delete_previous_file.called)

    @patch(
        "core_main_app.components.xsl_transformation.admin_site.delete_previous_file"
    )
    def test_staff_user_cannot_access_delete_file_view(
        self, mock_delete_previous_file
    ):
        """test_staff_user_cannot_access_delete_file_view"""
        xslt_id = 1
        index = 0
        url = reverse("admin:delete_file_xslt", args=[xslt_id, index])
        view = resolve(url).func
        response = RequestMock.do_request_get(
            view,
            param={"object_id": xslt_id, "index": index},
            user=self.staff_user,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(mock_delete_previous_file.called)

    @patch(
        "core_main_app.components.xsl_transformation.admin_site.delete_previous_file"
    )
    @patch("core_main_app.components.xsl_transformation.api.get_by_id")
    def test_superuser_can_access_delete_file_view(
        self, mock_get_xslt_by_id, mock_delete_previous_file
    ):
        """test_superuser_can_access_delete_file_view"""
        mock_get_xslt_by_id.return_value = MagicMock()
        xslt_id = 1
        index = 0
        url = reverse("admin:delete_file_xslt", args=[xslt_id, index])
        view = resolve(url).func
        response = RequestMock.do_request_get(
            view,
            param={"object_id": xslt_id, "index": index},
            user=self.superuser,
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(mock_delete_previous_file.called)

    @patch(
        "core_main_app.components.xsl_transformation.admin_site.utils_file_history_display"
    )
    def test_file_history_display_calls_utils_file_history_display(
        self, mock_utils_file_history_display
    ):
        """test_file_history_display_calls_utils_file_history_display

        Args:
            mock_utils_file_history_display:

        Returns:

        """
        # Arrange
        obj = MagicMock()
        custom_admin = CustomXslTransformationAdmin(
            XslTransformation, admin.AdminSite()
        )
        # Act
        custom_admin.file_history_display(obj)
        # Assert
        mock_utils_file_history_display.assert_called_once_with(
            obj,
            diff_url="admin:diff_file_xslt",
            delete_url="admin:delete_file_xslt",
        )

    @patch(
        "core_main_app.components.xsl_transformation.admin_site.xslt_api.get_by_id"
    )
    def test_diff_file_view_user_is_not_superuser(self, mock_get_by_id):
        """test_diff_file_view_user_is_not_superuser"""
        mock_request = MagicMock()
        mock_request.user = self.user
        object_id = 1
        index = 0
        view = CustomXslTransformationAdmin(
            XslTransformation, admin.AdminSite()
        ).diff_file_view
        response = view(mock_request, object_id, index)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch(
        "core_main_app.components.xsl_transformation.admin_site.xslt_api.get_by_id"
    )
    def test_diff_file_view_xsl_transformation_does_not_exist(
        self, mock_get_by_id
    ):
        """test_diff_file_view_xsl_transformation_does_not_exist"""
        mock_get_by_id.side_effect = DoesNotExist("Error")
        mock_request = MagicMock()
        mock_request.user = self.superuser
        object_id = 1
        index = 0
        view = CustomXslTransformationAdmin(
            XslTransformation, admin.AdminSite()
        ).diff_file_view
        response = view(mock_request, object_id, index)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("core_main_app.components.xsl_transformation.admin_site.diff_files")
    @patch(
        "core_main_app.components.xsl_transformation.admin_site.xslt_api.get_by_id"
    )
    def test_diff_file_view_success(self, mock_get_by_id, mock_diff_files):
        """test_diff_file_view_success"""
        mock_get_by_id.return_value = MagicMock()
        mock_diff_files.return_value = "diff"
        mock_request = MagicMock()
        mock_request.user = self.superuser
        object_id = 1
        index = 0
        view = CustomXslTransformationAdmin(
            XslTransformation, admin.AdminSite()
        ).diff_file_view
        response = view(mock_request, object_id, index)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        "core_main_app.components.xsl_transformation.admin_site.xslt_api.get_by_id"
    )
    def test_delete_file_view_user_is_not_superuser(self, mock_get_by_id):
        """test_delete_file_view_user_is_not_superuser"""
        mock_request = MagicMock()
        mock_request.user = self.user
        object_id = 1
        index = 0
        view = CustomXslTransformationAdmin(
            XslTransformation, admin.AdminSite()
        ).delete_file_view
        response = view(mock_request, object_id, index)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch(
        "core_main_app.components.xsl_transformation.admin_site.xslt_api.get_by_id"
    )
    def test_delete_file_view_xsl_transformation_does_not_exist(
        self, mock_get_by_id
    ):
        """test_delete_file_view_xsl_transformation_does_not_exist"""
        mock_get_by_id.side_effect = DoesNotExist("Error")
        mock_request = MagicMock()
        mock_request.user = self.superuser
        object_id = 1
        index = 0
        view = CustomXslTransformationAdmin(
            XslTransformation, admin.AdminSite()
        ).delete_file_view
        response = view(mock_request, object_id, index)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(
        "core_main_app.components.xsl_transformation.admin_site.xslt_api.get_by_id"
    )
    def test_diff_file_view_xslt_acl_error(self, mock_get_by_id):
        """test_diff_file_view_xslt_acl_error"""
        mock_get_by_id.side_effect = AccessControlError("Error")
        mock_request = MagicMock()
        mock_request.user = self.superuser
        object_id = 1
        index = 0
        view = CustomXslTransformationAdmin(
            XslTransformation, admin.AdminSite()
        ).diff_file_view
        response = view(mock_request, object_id, index)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch(
        "core_main_app.components.xsl_transformation.admin_site.xslt_api.get_by_id"
    )
    def test_delete_file_view_xslt_acl_error(self, mock_get_by_id):
        """test_delete_file_view_xslt_acl_error"""
        mock_get_by_id.side_effect = AccessControlError("Error")
        mock_request = MagicMock()
        mock_request.user = self.superuser
        object_id = 1
        index = 0
        view = CustomXslTransformationAdmin(
            XslTransformation, admin.AdminSite()
        ).delete_file_view
        response = view(mock_request, object_id, index)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestXslTransform(TestCase):
    """TestXslTransform"""

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transform_return_expected_string(self, mock_get_by_name):
        """test xsl transform return expected string

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")
        mock_xsl_path = join(mock_data_path, "transform.xsl")
        mock_html_path = join(mock_data_path, "data_transformed.html")

        with open(mock_xml_path, "r", encoding="utf-8") as xml_file:
            mock_xml_data = xml_file.read()

        mock_xslt = _create_mock_xsl_transformation(
            name="mock_xslt", filename="mock_xslt.xsl"
        )

        with open(mock_xsl_path, "r", encoding="utf-8") as xsl_file:
            mock_xslt.content = xsl_file.read()

        mock_get_by_name.return_value = mock_xslt

        with open(mock_html_path, "r", encoding="utf-8") as html_file:
            expected_result = html_file.read()

        # Act
        result = xsl_transformation_api.xsl_transform(
            mock_xml_data, mock_xslt.name
        )
        html_diff = htmldiff(
            result, expected_result
        )  # Computing difference in resulting content

        # Assert
        self.assertNotIn("<ins>", html_diff)
        self.assertNotIn("<del>", html_diff)

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transform_raise_api_error_on_encode_exception(
        self, mock_get_by_name
    ):
        """test xsl transform raise api error on encode exception

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")

        with open(mock_xml_path, "r", encoding="utf-8") as xml_file:
            mock_xml_data = xml_file.read()

        # two .encode() in a row will trigger the exception
        mock_xslt = _create_mock_xsl_transformation(
            name="mock_xslt",
            filename="mock_xslt.xsl",
            content="\u2000".encode("utf-8"),
        )

        mock_get_by_name.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.xsl_transform(mock_xml_data, mock_xslt.name)

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transform_raise_api_error_on_malformed_xslt(
        self, mock_get_by_name
    ):
        """test xsl transform raise api error on malformed xslt

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")

        with open(mock_xml_path, "r", encoding="utf-8") as xml_file:
            mock_xml_data = xml_file.read()

        mock_xslt = _create_mock_xsl_transformation(
            name="mock_xslt",
            filename="mock_xslt.xsl",
            content="mock_malformed_xslt/>",
        )
        mock_get_by_name.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.xsl_transform(mock_xml_data, mock_xslt.name)

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transform_raise_api_error_on_malformed_xml(
        self, mock_get_by_name
    ):
        """test xsl transform raise api error on malformed xml

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xsl_path = join(mock_data_path, "transform.xsl")

        mock_xml_data = "<tag>Unclosed"

        mock_xslt = _create_mock_xsl_transformation(
            name="mock_xslt", filename="mock_xslt.xsl"
        )

        with open(mock_xsl_path, "r", encoding="utf-8") as xsl_file:
            mock_xslt.content = xsl_file.read()

        mock_get_by_name.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.xsl_transform(mock_xml_data, mock_xslt.name)

    @patch.object(XslTransformation, "get_by_name")
    @patch("core_main_app.utils.xml.xsl_transform")
    def test_xsl_transform_raise_api_error_on_other_exception(
        self, mock_xsl_transform, mock_get_by_name
    ):
        """test xsl transform raise api error on other exception

        Args:
            mock_xsl_transform:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")
        mock_xsl_path = join(mock_data_path, "transform.xsl")

        with open(mock_xml_path, "r", encoding="utf-8") as xml_file:
            mock_xml_data = xml_file.read()

        mock_xslt = _create_mock_xsl_transformation(
            name="mock_xslt", filename="mock_xslt.xsl"
        )

        with open(mock_xsl_path, "r", encoding="utf-8") as xsl_file:
            mock_xslt.content = xsl_file.read()

        mock_get_by_name.return_value = mock_xslt
        mock_xsl_transform.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.xsl_transform(mock_xml_data, mock_xslt.name)


def _create_mock_xsl_transformation(name=None, filename=None, content=None):
    """create mock xsl transformation

    Args:
        name:
        filename:
        content:

    Returns:

    """
    mock_xslt = Mock(spec=XslTransformation)
    mock_xslt.name = name
    mock_xslt.filename = filename
    mock_xslt.content = content
    return mock_xslt


def _create_xsl_transformation(name=None, filename=None, content=None):
    """create xsl transformation

    Args:
        name:
        filename:
        content:

    Returns:

    """
    xsl_transformation = XslTransformation()
    xsl_transformation.name = name
    xsl_transformation.filename = filename
    xsl_transformation.content = content
    return xsl_transformation
