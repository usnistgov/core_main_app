""" Integration Test for Template Rest API
"""

from rest_framework import status
from tests.components.template.fixtures.fixtures import (
    AccessControlTemplateFixture,
)

from core_main_app.rest.template import views as template_rest_views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestTemplateDownload(IntegrationBaseTestCase):
    fixture = AccessControlTemplateFixture()

    def setUp(self):
        super(TestTemplateDownload, self).setUp()

    def test_get_returns_http_200(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            template_rest_views.TemplateDownload.as_view(),
            user,
            param={"pk": self.fixture.user1_template.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            template_rest_views.TemplateDownload.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_with_param_returns_http_200(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            template_rest_views.TemplateDownload.as_view(),
            user,
            param={"pk": self.fixture.user1_template.id},
            data={"pretty_print": "false"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_with_param_returns_formatted_content(self):
        # Arrange
        user = create_mock_user("1")
        expected_value = b'<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">\n  <xs:element name="tag"/>\n</xs:schema>\n'
        # Act
        response = RequestMock.do_request_get(
            template_rest_views.TemplateDownload.as_view(),
            user,
            param={"pk": self.fixture.user1_template.id},
            data={"pretty_print": "true"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, expected_value)
