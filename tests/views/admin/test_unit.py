""" Unit test views
"""
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.views.admin import views as admin_views
from core_main_app.views.admin.ajax import _get_xsd_content_from_html


class TestManageTemplates(SimpleTestCase):
    """Test Manage Templates"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1", is_staff=True)

    @patch("core_main_app.views.admin.views.admin_render")
    @patch(
        "core_main_app.components.template_version_manager.api.get_global_version_managers"
    )
    def test_get_manage_templates_returns_rendered_page(
        self,
        mock_get_global_version_managers,
        mock_admin_render,
    ):
        """test_get_manage_templates_returns_rendered_page

        Returns:

        """
        # Arrange
        request = self.factory.get("core_main_app_templates")
        request.user = self.user1

        mock_get_global_version_managers.return_value = []
        # Act
        response = admin_views.ManageTemplatesView.as_view()(request)

        # Assert
        self.assertTrue(response, mock_admin_render.return_value)
        self.assertTrue(mock_get_global_version_managers.called)


class TestGetXSDContentFromHTML(SimpleTestCase):
    """Test _get_xsd_content_from_html"""

    def test_get_xsd_content_from_html_returns_unescaped_string(self):
        """test_get_xsd_content_from_html_returns_unescaped_string

        Returns:

        """
        escaped_string = "&lt;xsd:schema&gt;&lt;/xsd:schema&gt;"
        expected_string = "<xsd:schema></xsd:schema>"
        self.assertEqual(
            _get_xsd_content_from_html(escaped_string), expected_string
        )
