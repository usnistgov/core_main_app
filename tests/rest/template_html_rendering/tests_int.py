""" Integration Test for TemplateHtmlRendering Rest API
"""

from unittest.mock import patch

from rest_framework import status
from tests.components.template_html_rendering.fixtures.fixtures import (
    TemplateHtmlRenderingFixtures,
)

from core_main_app.rest.template_html_rendering import views as rest_views
from core_main_app.components.template_html_rendering import (
    api as template_html_rendering_api,
)
from core_main_app.rest.template_html_rendering.views import (
    BaseDataHtmlRender,
)
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import (
    RequestMock,
    create_mock_request,
)

fixture_template_html_rendering = TemplateHtmlRenderingFixtures()


class TestGetTemplateHtmlRenderingList(IntegrationBaseTestCase):
    """TestGetTemplateHtmlRenderingList"""

    fixture = fixture_template_html_rendering

    def setUp(self):
        """setUp

        Returns:

        """
        self.user = create_mock_user("1", is_superuser=True, is_staff=True)
        super().setUp()

    def test_get_all_returns_status_403_without_permission(self):
        """test_get_all_returns_status_403_without_permission

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            rest_views.TemplateHtmlRenderingList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_html_rendering_api, "get_all")
    def test_get_all_raises_500_sever_error_when_general_error_occurred(
        self, mock_get_all
    ):
        """test_get_all_raises_500_sever_error_when_general_error_occurred

        Returns:

        """
        mock_get_all.side_effect = Exception("test_raises_error")
        # Act
        response = RequestMock.do_request_get(
            rest_views.TemplateHtmlRenderingList.as_view(), self.user
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_get_returns_http_200(self):
        """test_get_returns_http_200

        Returns:

        """

        # Act
        response = RequestMock.do_request_get(
            rest_views.TemplateHtmlRenderingList.as_view(), self.user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_template_html_rendering_returns_list(self):
        """test_get_all_template_html_rendering_returns_list

        Returns:

        """

        # Act
        response = RequestMock.do_request_get(
            rest_views.TemplateHtmlRenderingList.as_view(), self.user
        )

        # Assert
        self.assertEqual(len(response.data), 3)


class TestPostTemplateHtmlRenderingList(IntegrationBaseTestCase):
    """TestPostTemplateHtmlRenderingList"""

    fixture = fixture_template_html_rendering

    def setUp(self):
        """setUp

        Returns:

        """
        self.user = create_mock_user("1", is_superuser=True, is_staff=True)
        super().setUp()

    def test_post_returns_http_201(self):
        """test_post_returns_http_201

        Returns:

        """
        # Context

        mock_data = {"template": self.fixture.template_3.id}

        # Act
        response = RequestMock.do_request_post(
            rest_views.TemplateHtmlRenderingList.as_view(),
            self.user,
            data=mock_data,
        )
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_creates_template_html_rendering(self):
        """test_post_creates_template_html_rendering

        Returns:

        """
        # Context
        mock_data = {
            "template": self.fixture.template_3.id,
            "list_rendering": "test",
            "detail_rendering": "test",
        }

        # Act
        RequestMock.do_request_post(
            rest_views.TemplateHtmlRenderingList.as_view(),
            self.user,
            data=mock_data,
        )

        # Assert
        template_html_rendering = (
            template_html_rendering_api.get_by_template_id(
                self.fixture.template_3.id
            )
        )
        self.assertEqual(
            template_html_rendering.template, self.fixture.template_3
        )
        self.assertEqual(template_html_rendering.list_rendering, "test")
        self.assertEqual(template_html_rendering.detail_rendering, "test")

    def test_post_without_list_and_detail_rendering_creates_template_html_rendering(
        self,
    ):
        """test_post_without_list_and_detail_rendering_creates_template_html_rendering

        Returns:

        """
        # Context
        mock_data = {"template": self.fixture.template_3.id}

        # Act
        RequestMock.do_request_post(
            rest_views.TemplateHtmlRenderingList.as_view(),
            self.user,
            data=mock_data,
        )

        # Assert
        template_html_rendering = (
            template_html_rendering_api.get_by_template_id(
                self.fixture.template_3.id
            )
        )
        self.assertEqual(
            template_html_rendering.template, self.fixture.template_3
        )
        self.assertEqual(template_html_rendering.list_rendering, "")
        self.assertEqual(template_html_rendering.detail_rendering, "")

    def test_post_returns_status_400_when_template_missing(self):
        """test_post_returns_status_400_when_template_missing

        Returns:

        """
        # Context
        mock_data = {"list_rendering": "test", "detail_rendering": "test"}

        # Act
        response = RequestMock.do_request_post(
            rest_views.TemplateHtmlRenderingList.as_view(),
            self.user,
            data=mock_data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            "field is required" in response.rendered_content.decode("utf-8")
        )

    def test_post_returns_http_400_when_template_already_linked_to_another_template_html_rendering(
        self,
    ):
        """test_post_returns_http_400_when_template_already_linked_to_another_template_html_rendering

        Returns:

        """
        # Context
        mock_data = {"template": self.fixture.template_1.id}

        # Act
        response = RequestMock.do_request_post(
            rest_views.TemplateHtmlRenderingList.as_view(),
            self.user,
            data=mock_data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            "template html rendering with this template already exists"
            in response.rendered_content.decode("utf-8")
        )

    @patch(
        "core_main_app.rest.template_html_rendering.views.TemplateHtmlRenderingSerializer.save"
    )
    def test_get_all_raises_500_sever_error_when_general_error_occurred(
        self, mock_get_all
    ):
        """test_get_all_raises_500_sever_error_when_general_error_occurred

        Returns:

        """
        # Context
        mock_data = {"template": self.fixture.template_3.id}
        mock_get_all.side_effect = Exception("test_raises_error")
        # Act
        response = RequestMock.do_request_post(
            rest_views.TemplateHtmlRenderingList.as_view(),
            self.user,
            data=mock_data,
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestGetTemplateHtmlRenderingDetail(IntegrationBaseTestCase):
    """TestGetTemplateHtmlRenderingDetail"""

    fixture = fixture_template_html_rendering

    def setUp(self):
        """setUp

        Returns:

        """
        self.user = create_mock_user("1", is_superuser=True, is_staff=True)
        super().setUp()

    def test_get_returns_object_when_found(self):
        """test_get_returns_object_when_found

        Returns:

        """
        # Arrange
        self.param = {"pk": self.fixture.template_html_rendering_1.id}

        # Act
        response = RequestMock.do_request_get(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            self.user,
            None,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_raise_404_when_not_found(self):
        """test_get_raise_404_when_not_found

        Returns:

        """
        # Arrange
        self.param = {"pk": -1}

        # Act
        response = RequestMock.do_request_get(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            self.user,
            None,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_raise_500_sever_error_when_general_error_occurred(self):
        """test_get_raise_500_sever_error_when_general_error_occurred

        Returns:

        """
        # Arrange
        self.param = {"pk": "test"}

        # Act
        response = RequestMock.do_request_get(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            self.user,
            None,
            self.param,
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestDeleteTemplateHtmlRenderingDetail(IntegrationBaseTestCase):
    """TestDeleteTemplateHtmlRenderingDetail"""

    fixture = fixture_template_html_rendering

    def setUp(self):
        """setUp

        Returns:

        """
        self.user = create_mock_user("1", is_superuser=True, is_staff=True)
        super().setUp()

    def test_delete_raises_403_if_user_is_unauthorized(self):
        """test_delete_raises_403_if_user_is_unauthorized

        Returns:

        """
        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": 1}

        # Act
        response = RequestMock.do_request_delete(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            user,
            None,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_raises_404_when_not_found(self):
        """test_delete_raises_404_when_not_found

        Returns:

        """
        # Arrange
        self.param = {"pk": -1}

        # Act
        response = RequestMock.do_request_delete(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            self.user,
            None,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_raises_500_sever_error_when_general_error_occurred(self):
        """test_delete_raises_500_sever_error_when_general_error_occurred

        Returns:

        """
        # Arrange
        self.param = {"pk": "test"}

        # Act
        response = RequestMock.do_request_delete(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            self.user,
            None,
            self.param,
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_delete_returns_204_if_document_is_deleted_with_success(self):
        """test_delete_returns_204_if_document_is_deleted_with_success

        Returns:

        """
        # Arrange
        self.param = {"pk": self.fixture.template_html_rendering_1.id}

        # Act
        response = RequestMock.do_request_delete(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            self.user,
            None,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestPatchTemplateHtmlRenderingDetail(IntegrationBaseTestCase):
    """TestPatchTemplateHtmlRenderingDetail"""

    fixture = fixture_template_html_rendering

    def setUp(self):
        """setUp

        Returns:

        """
        self.user = create_mock_user("1", is_superuser=True, is_staff=True)
        super().setUp()
        self.data = None

    def test_patch_raises_403_if_user_is_authorized(self):
        """test_patch_raises_403_if_user_is_authorized

        Returns:

        """
        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": 1}

        # Act
        response = RequestMock.do_request_patch(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_raises_404_when_not_found(self):
        """test_patch_raises_404_when_not_found

        Returns:

        """
        # Arrange
        self.param = {"pk": -1}

        # Act
        response = RequestMock.do_request_patch(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            self.user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_raises_400_sever_error_when_general_error_occurred(self):
        """test_patch_raises_400_sever_error_when_general_error_occurred

        Returns:

        """
        # Arrange
        self.param = {"pk": self.fixture.template_html_rendering_1.id}

        # Act
        response = RequestMock.do_request_patch(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            self.user,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_raises_400_sever_error_when_template_updated(self):
        """test_patch_raise_400_sever_error_when_template_updated

        Returns:

        """
        # Arrange
        self.param = {"pk": self.fixture.template_html_rendering_1.id}
        self.data = {
            "list_rendering": "updated",
            "detail_rendering": "updated",
            "template": self.fixture.template_3.id,
        }

        # Act
        response = RequestMock.do_request_patch(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            self.user,
            param=self.param,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            "Template can not be updated"
            in response.rendered_content.decode("utf-8")
        )

    def test_patch_raises_500_sever_error_when_general_error_occurred(self):
        """test_patch_raises_500_sever_error_when_general_error_occurred

        Returns:

        """
        # Arrange
        self.param = {"pk": "test"}

        # Act
        response = RequestMock.do_request_patch(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            self.user,
            None,
            self.param,
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_patch_returns_200_when_data_are_valid_with_authorized_user(self):
        """test_patch_returns_200_when_data_are_valid_with_authorized_user

        Returns:

        """
        # Arrange
        self.param = {"pk": self.fixture.template_html_rendering_1.id}

        self.data = {
            "list_rendering": "updated",
            "detail_rendering": "updated",
        }

        self.assertEqual(
            self.fixture.template_html_rendering_1.list_rendering,
            "<b>Title:<b/>{{dict_content.root.title}}",
        )
        self.assertEqual(
            self.fixture.template_html_rendering_1.detail_rendering,
            "detail_rendering_1",
        )

        # Act
        response = RequestMock.do_request_patch(
            rest_views.TemplateHtmlRenderingDetail.as_view(),
            self.user,
            self.data,
            self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["list_rendering"], "updated")
        self.assertEqual(response.data["detail_rendering"], "updated")


class TestBaseDataHtmlRender(IntegrationBaseTestCase):
    """Test Base Data Html Render"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.request = create_mock_request(create_mock_user("1"))

    def test_format_raises_not_implemented_error(self):
        """test_format_raises_not_implemented_error

        Returns:

        """
        # Assert
        with self.assertRaises(NotImplementedError):
            BaseDataHtmlRender.get_object(self, "1", self.request)
