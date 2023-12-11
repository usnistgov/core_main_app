"""Unit tests for data rest api
"""
from unittest.mock import patch, MagicMock, mock_open

from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError
from tests.components.data.fixtures.fixtures import QueryDataFixtures
from tests.components.data.tests_unit import _get_template, _get_json_template
from tests.mocks import MockQuerySet

from core_main_app.commons.exceptions import DoesNotExist, RestApiError
from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.template import api as template_api
from core_main_app.components.template.models import Template
from core_main_app.components.workspace.models import Workspace
from core_main_app.rest.data import views as data_rest_views
from core_main_app.rest.data.abstract_views import (
    AbstractExecuteLocalQueryView,
)
from core_main_app.rest.data.admin_serializers import AdminDataSerializer
from core_main_app.rest.data.serializers import DataSerializer
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import (
    RequestMock,
    create_mock_request,
)


class TestDataList(SimpleTestCase):
    """TestDataList"""

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        self.data = {
            "template": None,
            "user_id": "1",
            "xml_content": "test",
            "title": "test",
        }

    @patch.object(Data, "get_all_by_user_id")
    def test_get_all_returns_http_200(self, mock_get_all):
        """test_get_all_returns_http_200

        Args:
            mock_get_all:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_all.return_value = MockQuerySet()

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(), mock_user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_returns_http_400_if_invalid_data(self):
        """test_post_returns_http_400_if_invalid_data

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")

        # Mock
        response = RequestMock.do_request_post(
            data_rest_views.DataList.as_view(), mock_user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDataDetail(SimpleTestCase):
    """TestDataDetail"""

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    @patch.object(Data, "get_by_id")
    def test_get_returns_http_404_when_data_not_found(self, mock_get_by_id):
        """test_get_returns_http_404_when_data_not_found

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_by_id.side_effect = DoesNotExist("error")

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": "1"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(Data, "get_by_id")
    def test_get_returns_data_when_exists(self, mock_get_by_id):
        """test_get_returns_data_when_exists

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_by_id.return_value = _create_data("test")

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": "1"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Data, "get_by_id")
    def test_get_returns_data_with_template_info_when_exists(
        self, mock_get_by_id
    ):
        """test_get_returns_data_with_template_info_when_exists

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_by_id.return_value = _create_data("test")

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(),
            mock_user,
            param={"pk": "1"},
            data={"template_info": "true"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("content" in response.data["template"])

    @patch.object(Data, "get_by_id")
    def test_get_returns_data_with_template_info_false_does_not_return_info(
        self, mock_get_by_id
    ):
        """test_get_returns_data_with_template_info_false_does_not_return_info

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_by_id.return_value = _create_data("test")

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(),
            mock_user,
            param={"pk": "1"},
            data={"template_info": "false"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["template"])

    @patch.object(Data, "get_by_id")
    def test_get_returns_data_without_template_info_param_does_not_return_info(
        self, mock_get_by_id
    ):
        """test_get_returns_data_without_template_info_param_does_not_return_info

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_by_id.return_value = _create_data("test")

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(),
            mock_user,
            param={"pk": "1"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["template"])

    @patch.object(Data, "get_by_id")
    def test_delete_returns_http_404_when_data_not_found(self, mock_get_by_id):
        """test_delete_returns_http_404_when_data_not_found

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_by_id.side_effect = DoesNotExist("error")

        # Mock
        response = RequestMock.do_request_delete(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": "1"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(Data, "get_by_id")
    def test_patch_returns_http_404_when_data_not_found(self, mock_get_by_id):
        """test_patch_returns_http_404_when_data_not_found

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_by_id.side_effect = DoesNotExist("error")

        # Mock
        response = RequestMock.do_request_patch(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": "1"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(Data, "get_by_id")
    @patch("core_main_app.components.data.api.upsert")
    def test_patch_returns_http_400_when_no_update_data_provided(
        self, mock_get_by_id, mock_upsert
    ):
        """test_patch_returns_http_400_when_no_update_data_provided

        Args:
            mock_get_by_id:
            mock_upsert:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_data = Data(user_id="1")
        mock_get_by_id.return_value = mock_data
        mock_upsert.return_value = mock_data

        # Mock
        response = RequestMock.do_request_patch(
            data_rest_views.DataDetail.as_view(), mock_user, param={"pk": "1"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDataDownload(SimpleTestCase):
    """TestDataDownload"""

    fixture_data = QueryDataFixtures()

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    @patch.object(Data, "get_by_id")
    def test_get_returns_http_404_when_data_not_found(self, mock_get_by_id):
        """test_get_returns_http_404_when_data_not_found

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_by_id.side_effect = DoesNotExist("error")

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(),
            mock_user,
            param={"pk": "1"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(data_api, "get_by_id")
    def test_get_returns_http_200_when_data_found(
        self, mock_data_api_get_by_id
    ):
        """test_get_returns_http_200_when_data_found

        Args:
            mock_data_api_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_data = _create_data()
        mock_data_api_get_by_id.return_value = mock_data

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(),
            mock_user,
            param={"pk": "1"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_by_id")
    def test_get_returns_http_400_when_data_not_well_formatted(
        self, mock_data_api_get_by_id
    ):
        """test_get_returns_http_400_when_data_not_well_formatted

        Args:
            mock_data_api_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_data = _create_data()
        # remove last character from data
        mock_data.content = mock_data.content[:-1]
        mock_data_api_get_by_id.return_value = mock_data

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(),
            mock_user,
            param={"pk": "1"},
            data={"pretty_print": "true"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(data_api, "get_by_id")
    def test_get_without_pretty_print_returns_data(
        self, mock_data_api_get_by_id
    ):
        """test_get_without_pretty_print_returns_data

        Args:
            mock_data_api_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_data = _create_data()
        mock_data_api_get_by_id.return_value = mock_data
        expected_value = b'<root  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ><string>x</string></root>'
        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(),
            mock_user,
            param={"pk": "1"},
            data={"pretty_print": "false"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected_value)

    @patch.object(data_api, "get_by_id")
    def test_get_with_pretty_print_returns_formatted_data(
        self, mock_data_api_get_by_id
    ):
        """test_get_with_pretty_print_returns_formatted_data

        Args:
            mock_data_api_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_data = _create_data()
        mock_data_api_get_by_id.return_value = mock_data
        expected_value = b'<root xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n  <string>x</string>\n</root>\n'

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(),
            mock_user,
            param={"pk": "1"},
            data={"pretty_print": "true"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected_value)

    @patch.object(data_api, "get_by_id")
    def test_get_with_pretty_print_json_returns_formatted_data(
        self, mock_data_api_get_by_id
    ):
        """test_get_with_pretty_print_returns_formatted_data

        Args:
            mock_data_api_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_data = _create_json_data()
        mock_data_api_get_by_id.return_value = mock_data
        expected_value = b'{\n  "root": {\n    "string": "x"\n  }\n}'

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(),
            mock_user,
            param={"pk": "1"},
            data={"pretty_print": "true"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected_value)

    @patch.object(data_api, "get_by_id")
    def test_get_with_pretty_unknown_template_format_return_bad_response(
        self, mock_data_api_get_by_id
    ):
        """test_get_with_pretty_unknown_template_format_return_bad_response

        Args:
            mock_data_api_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_data = _create_data()
        mock_data.template.format = "BAD"
        mock_data_api_get_by_id.return_value = mock_data

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(),
            mock_user,
            param={"pk": "1"},
            data={"pretty_print": "true"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDataPermissions(SimpleTestCase):
    """TestDataPermissions"""

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    @patch.object(Data, "get_by_id")
    def test_get_returns_http_404_when_data_not_found(self, mock_get_by_id):
        """test_get_returns_http_404_when_data_not_found

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")
        mock_get_by_id.side_effect = DoesNotExist("error")

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            mock_user,
            data={"ids": '["1"]'},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(Data, "get_by_id")
    def test_get_returns_permissions_for_superuser(self, mock_get_by_id):
        """test_get_returns_permissions_for_superuser

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_data = Data(user_id="1")
        mock_get_by_id.return_value = mock_data

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            mock_user,
            data={"ids": '["1"]'},
        )

        # Assert
        excepted_result = {"1": True}
        self.assertEqual(response.data, excepted_result)

    @patch.object(Data, "get_by_id")
    def test_get_returns_permissions_for_owner(self, mock_get_by_id):
        """test_get_returns_permissions_for_owner

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_staff=True)
        mock_data = Data(user_id="1")
        mock_get_by_id.return_value = mock_data

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            mock_user,
            data={"ids": '["1"]'},
        )

        # Assert
        excepted_result = {"1": True}
        self.assertEqual(response.data, excepted_result)

    @patch.object(Data, "get_by_id")
    def test_get_returns_permissions_for_non_owner(self, mock_get_by_id):
        """test_get_returns_permissions_for_non_owner

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("2", is_staff=True)
        mock_data = Data(user_id="1")
        mock_get_by_id.return_value = mock_data

        # Mock
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            mock_user,
            data={"ids": '["1"]'},
        )

        # Assert
        excepted_result = {"1": False}
        self.assertEqual(response.data, excepted_result)


class TestBulkUploadFolder(SimpleTestCase):
    """Test Bulk Upload Folder"""

    def setUp(self):
        """setUp"""

        super().setUp()

    def test_put_not_staff_return_http_403(
        self,
    ):
        """test_put_not_staff_return_http_403

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")

        # Mock
        response = RequestMock.do_request_put(
            data_rest_views.BulkUploadFolder.as_view(),
            mock_user,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_api, "get_by_id")
    def test_put_folder_bad_template_id_return_http_404(
        self, mock_template_api_get_by_id
    ):
        """test_put_folder_bad_template_id_return_http_404

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_staff=True)
        mock_template_api_get_by_id.side_effect = DoesNotExist("error")

        # Mock
        response = RequestMock.do_request_put(
            data_rest_views.BulkUploadFolder.as_view(),
            mock_user,
            data={"folder": "folder", "template": "1", "workspace": "1"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(data_rest_views.BulkUploadFolder, "_bulk_create")
    @patch("builtins.open", new_callable=mock_open, read_data=b"<tag></tag>")
    @patch("core_main_app.components.data.api.check_json_file_is_valid")
    @patch("core_main_app.components.data.api.check_xml_file_is_valid")
    @patch("os.listdir")
    @patch("os.path.exists")
    @patch.object(template_api, "get_by_id")
    def test_put_xml_folder_calls_xml_validation(
        self,
        mock_template_api_get_by_id,
        mock_exists,
        mock_list_dir,
        mock_check_xml_file_is_valid,
        mock_check_json_file_is_valid,
        mock_open_func,
        mock_bulk_create,
    ):
        """test_put_xml_folder_calls_xml_validation

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_staff=True)
        mock_template_api_get_by_id.return_value = MagicMock(
            format=Template.XSD
        )
        mock_exists.return_value = True
        mock_list_dir.return_value = [MagicMock()]
        mock_check_xml_file_is_valid.return_value = True
        mock_check_json_file_is_valid.return_value = True
        mock_bulk_create.return_value = None

        # Mock
        response = RequestMock.do_request_put(
            data_rest_views.BulkUploadFolder.as_view(),
            mock_user,
            data={"folder": "folder", "template": "1", "workspace": "1"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_check_xml_file_is_valid.called)
        self.assertFalse(mock_check_json_file_is_valid.called)

    @patch.object(data_rest_views.BulkUploadFolder, "_bulk_create")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=b'{"element": "value"}',
    )
    @patch("core_main_app.components.data.api.check_json_file_is_valid")
    @patch("core_main_app.components.data.api.check_xml_file_is_valid")
    @patch("os.listdir")
    @patch("os.path.exists")
    @patch.object(template_api, "get_by_id")
    def test_put_json_folder_calls_json_validation(
        self,
        mock_template_api_get_by_id,
        mock_exists,
        mock_list_dir,
        mock_check_xml_file_is_valid,
        mock_check_json_file_is_valid,
        mock_open_func,
        mock_bulk_create,
    ):
        """test_put_json_folder_calls_json_validation

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_staff=True)
        mock_template_api_get_by_id.return_value = MagicMock(
            format=Template.JSON
        )
        mock_exists.return_value = True
        mock_list_dir.return_value = [MagicMock()]
        mock_check_xml_file_is_valid.return_value = True
        mock_check_json_file_is_valid.return_value = True
        mock_bulk_create.return_value = None

        # Mock
        response = RequestMock.do_request_put(
            data_rest_views.BulkUploadFolder.as_view(),
            mock_user,
            data={"folder": "folder", "template": "1", "workspace": "1"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(mock_check_xml_file_is_valid.called)
        self.assertTrue(mock_check_json_file_is_valid.called)


class TestDataSerializer(SimpleTestCase):
    """TestDataSerializer"""

    @patch("core_main_app.components.data.api.upsert")
    @patch.object(Template, "get_by_id")
    def test_data_serializer_create_data(
        self, mock_template_get_by_id, mock_data_upsert
    ):
        """test_data_serializer_create_data

        Args:
            mock_template_get_by_id:
            mock_data_upsert:

        Returns:

        """
        # Arrange
        mock_template = _get_template()
        mock_workspace = Workspace(id=1)
        mock_template_get_by_id.return_value = mock_template
        data_serializer = DataSerializer()
        data_serializer.context["request"] = create_mock_request(
            user=create_mock_user("1")
        )
        mock_data = _create_data()
        mock_data_upsert.return_value = mock_data

        # Act
        data_serializer.create(
            validated_data={
                "template": mock_template,
                "workspace": mock_workspace,
                "title": "test",
                "content": "<tag></tag>",
            }
        )

        # Assert
        self.assertTrue(mock_data_upsert.called)

    @patch("core_main_app.components.data.api.upsert")
    def test_data_serializer_update_data(self, mock_data_upsert):
        """test_data_serializer_update_data

        Args:
            mock_data_upsert:

        Returns:

        """
        # Arrange
        data_serializer = DataSerializer()
        data_serializer.context["request"] = create_mock_request(
            user=create_mock_user("1")
        )
        mock_data = _create_data()
        mock_data_upsert.return_value = mock_data

        # Act
        data_serializer.update(
            instance=mock_data,
            validated_data={
                "title": "test",
                "content": "<tag></tag>",
            },
        )

        # Assert
        self.assertTrue(mock_data_upsert.called)

    @patch("core_main_app.components.data.api.upsert")
    def test_data_serializer_with_xml_content_update_data(
        self, mock_data_upsert
    ):
        """test_data_serializer_with_xml_content_update_data

        Args:
            mock_data_upsert:

        Returns:

        """
        # Arrange
        data_serializer = DataSerializer()
        data_serializer.context["request"] = create_mock_request(
            user=create_mock_user("1")
        )
        mock_data = _create_data()
        mock_data_upsert.return_value = mock_data

        # Act
        data_serializer.update(
            instance=mock_data,
            validated_data={
                "title": "test",
                "xml_content": "<tag></tag>",
            },
        )

        # Assert
        self.assertTrue(mock_data_upsert.called)

    @patch("core_main_app.components.data.api.admin_insert")
    @patch.object(Template, "get_by_id")
    def test_admin_data_serializer_create_data(
        self, mock_template_get_by_id, mock_admin_insert
    ):
        """test_data_serializer_create_data

        Args:
            mock_template_get_by_id:
            mock_admin_insert:

        Returns:

        """
        # Arrange
        mock_template = _get_template()
        mock_workspace = Workspace(id=1)
        mock_template_get_by_id.return_value = mock_template
        data_serializer = AdminDataSerializer()
        data_serializer.context["request"] = create_mock_request(
            user=create_mock_user("1", is_superuser=True, is_staff=True)
        )
        mock_data = _create_data()
        mock_admin_insert.return_value = mock_data

        # Act
        data_serializer.create(
            validated_data={
                "template": mock_template,
                "workspace": mock_workspace,
                "title": "test",
                "content": "<tag></tag>",
            }
        )

        # Assert
        self.assertTrue(mock_admin_insert.called)

    @patch.object(Data, "convert_and_save")
    @patch.object(Template, "get_by_id")
    def test_data_serializer_with_xml_content(
        self, mock_template_get_by_id, mock_data_convert_and_save
    ):
        """test_data_serializer_with_xml_content

        Args:
            mock_template_get_by_id:
            mock_data_convert_and_save:

        Returns:

        """
        # Arrange
        mock_template = _get_template()
        mock_workspace = Workspace(id=1)
        mock_template_get_by_id.return_value = mock_template
        data_serializer = DataSerializer()
        data_serializer.context["request"] = create_mock_request(
            user=create_mock_user("1", is_superuser=True)
        )

        mock_data_convert_and_save.return_value = None
        new_xml_content = "<tag></tag>"

        # Act
        serialized_data = data_serializer.create(
            validated_data={
                "template": mock_template,
                "workspace": mock_workspace,
                "title": "test",
                "xml_content": new_xml_content,
            }
        )

        # Assert
        self.assertEqual(serialized_data.content, new_xml_content)

    @patch.object(Template, "get_by_id")
    def test_data_serializer_without_xml_content_or_content_fails(
        self, mock_template_get_by_id
    ):
        """test_data_serializer_without_xml_content_or_content_fails

        Args:
            mock_template_get_by_id:

        Returns:

        """
        # Arrange
        mock_template = _get_template()
        mock_workspace = Workspace(id=1)
        mock_template_get_by_id.return_value = mock_template
        data_serializer = DataSerializer(
            data={
                "template": mock_template,
                "workspace": mock_workspace,
                "title": "test",
            }
        )
        data_serializer.context["request"] = create_mock_request(
            user=create_mock_user("1", is_superuser=True)
        )
        # Act + Assert
        with self.assertRaises(ValidationError):
            data_serializer.is_valid(raise_exception=True)

    def test_data_serializer_with_content_only_succeeds(
        self,
    ):
        """test_data_serializer_with_content_only_succeeds

        Args:

        Returns:

        """
        # Arrange
        data_serializer = DataSerializer()
        data_serializer.context["request"] = create_mock_request(
            user=create_mock_user("1", is_superuser=True)
        )

        # Act
        attrs = data_serializer.validate(
            attrs={
                "title": "test",
                "content": "<tag></tag>",
            }
        )
        # Assert
        self.assertTrue("content" in attrs)

    def test_data_serializer_with_xmL_content_only_succeeds(
        self,
    ):
        """test_data_serializer_with_xmL_content_only_succeeds

        Args:

        Returns:

        """
        # Arrange
        data_serializer = DataSerializer()
        data_serializer.context["request"] = create_mock_request(
            user=create_mock_user("1", is_superuser=True)
        )

        # Act
        attrs = data_serializer.validate(
            attrs={
                "title": "test",
                "xml_content": "<tag></tag>",
            }
        )
        # Assert
        self.assertTrue("xml_content" in attrs)


class TestAbstractExecuteLocalQueryView(SimpleTestCase):
    """TestAbstractExecuteLocalQueryView"""

    def test_parse_id_with_template_obj(
        self,
    ):
        """test_parse_id_with_template_obj

        Args:


        Returns:

        """
        # Arrange
        mock_template = _get_template()

        # Act
        result = AbstractExecuteLocalQueryView.parse_id(mock_template)

        # Assert
        self.assertEqual(result, mock_template.id)

    def test_parse_id_with_template_dict(
        self,
    ):
        """test_parse_id_with_template_dict

        Args:


        Returns:

        """
        # Arrange
        mock_template_dict = {"id": 1}

        # Act
        result = AbstractExecuteLocalQueryView.parse_id(mock_template_dict)

        # Assert
        self.assertEqual(result, mock_template_dict["id"])

    def test_parse_id_with_template_dict_no_id_field_raises_exception(
        self,
    ):
        """test_parse_id_with_template_dict_no_id_field_raises_exception

        Args:


        Returns:

        """
        # Arrange
        mock_template_dict = {"test": 1}

        # Act
        with self.assertRaises(RestApiError):
            AbstractExecuteLocalQueryView.parse_id(mock_template_dict)


def _create_data(title="test"):
    """Create an XML data

    Args:
        title:

    Returns:
    """
    template = _get_template()
    data = Data(title=title, template=template, user_id="1")
    data.xml_content = '<root  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ><string>x</string></root>'
    return data


def _create_json_data(title="test"):
    """Create a JSON data

    Args:
        title:

    Returns:
    """
    template = _get_json_template()
    data = Data(title=title, template=template, user_id="1")
    data.content = {"root": {"string": "x"}}
    return data
