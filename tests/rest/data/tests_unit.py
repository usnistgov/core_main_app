"""Unit tests for data rest api
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.data.models import Data
from core_main_app.rest.data import views as data_rest_views
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


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
        mock_get_all.return_value = []

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
            data_rest_views.DataDownload.as_view(), mock_user, param={"pk": "1"}
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
            data_rest_views.DataPermissions.as_view(), mock_user, data={"ids": '["1"]'}
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
            data_rest_views.DataPermissions.as_view(), mock_user, data={"ids": '["1"]'}
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
            data_rest_views.DataPermissions.as_view(), mock_user, data={"ids": '["1"]'}
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
            data_rest_views.DataPermissions.as_view(), mock_user, data={"ids": '["1"]'}
        )

        # Assert
        excepted_result = {"1": False}
        self.assertEqual(response.data, excepted_result)
