""" Unit test views
"""
from unittest.mock import patch, MagicMock

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, SimpleTestCase, override_settings

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.user_preferences.models import UserPreferences
from core_main_app.utils import xml
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.views.common.views import (
    DataXMLEditor,
    XmlEditor,
    JSONEditor,
)
from core_main_app.views.user.views import (
    set_timezone,
    custom_login,
    custom_logout,
)


class TestXmlEditorGenerateView(SimpleTestCase):
    """Test Xml Editor Generate View"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")

    @override_settings(INSTALLED_APPS=["core_curate_app", "core_parser_app"])
    @patch(
        "core_curate_app.components.curate_data_structure.models.CurateDataStructure"
    )
    @patch("core_main_app.utils.xml.format_content_xml")
    @patch("core_curate_app.views.user.views.render_xml")
    @patch("core_parser_app.components.data_structure_element.api.get_by_id")
    @patch("core_parser_app.tools.parser.parser.XSDParser.generate_form")
    @patch("core_curate_app.components.curate_data_structure.api.delete")
    @patch("core_curate_app.components.curate_data_structure.api.upsert")
    @patch("core_main_app.components.template.api.get_by_id")
    def test_generate_returns_response_with_xml(
        self,
        mock_template_get_by_id,
        mock_curate_ds_upsert,
        mock_curate_ds_delete,
        mock_generate_form,
        mock_dse_get_by_id,
        mock_render_xml,
        mock_format_xml,
        mock_curate_ds,
    ):
        """test_generate_with_content_returns_error

        Returns:

        """
        # Arrange
        mock_template_get_by_id.return_value = MagicMock(content="")
        mock_curate_ds_upsert.return_value = None
        mock_curate_ds_delete.return_value = None
        mock_generate_form.return_value = 1
        mock_dse_get_by_id.return_value = MagicMock()
        mock_render_xml.return_value = "<root></root>"
        mock_format_xml.return_value = "<root/>"
        mock_curate_ds.return_value = MagicMock()

        request = self.factory.get("core_main_app_xml_text_editor_view")
        request.user = self.user1
        data = {
            "content": "",
            "template_id": "1",
            "action": "generate",
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)
        request.user = self.user1

        # Act
        response = DataXMLEditor.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_template_get_by_id.called)
        self.assertTrue(mock_curate_ds_upsert.called)
        self.assertTrue(mock_generate_form.called)
        self.assertTrue(mock_dse_get_by_id.called)
        self.assertTrue(mock_render_xml.called)
        self.assertTrue(mock_format_xml.called)
        self.assertTrue(mock_curate_ds.called)

    @override_settings(INSTALLED_APPS=["core_curate_app"])
    def test_generate_with_content_returns_error(self):
        """test_generate_with_content_returns_error

        Returns:

        """
        request = self.factory.get("core_main_app_xml_text_editor_view")
        request.user = self.user1
        data = {
            "content": "<root></root>",
            "template_id": "1",
            "action": "generate",
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)
        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            b"Please clear form before generating a new XML document.",
        )

    def test_generate_without_core_curate_app_returns_error(self):
        """test_generate_without_core_curate_app_returns_error

        Returns:

        """
        request = self.factory.get("core_main_app_xml_text_editor_view")
        request.user = self.user1
        data = {
            "content": "",
            "template_id": "1",
            "action": "generate",
        }
        request = self.factory.post("core_main_app_xml_text_editor_view", data)
        request.user = self.user1
        response = DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            b"The Curate App needs to be installed to use this feature.",
        )


class TestSetTimezone(SimpleTestCase):
    """TestSetTimezone"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    def test_get_when_user_has_preferences_returns_form(
        self, mock_get_by_user
    ):
        """test_get_when_user_has_preferences_returns_form

        Returns:

        """
        # Arrange
        mock_get_by_user.return_value = UserPreferences(
            user_id="1", timezone="GMT"
        )
        request = self.factory.get("core_main_set_timezone")
        request.user = self.user1

        # Act
        response = set_timezone(request)

        # Assert
        self.assertTrue("form" in response.content.decode())
        self.assertTrue(
            '<option value="GMT" selected>GMT</option>'
            in response.content.decode()
        )

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    def test_get_returns_form(self, mock_get_by_user):
        """test_get_returns_form

        Returns:

        """
        # Arrange
        mock_get_by_user.return_value = UserPreferences(
            user_id="1", timezone="Africa/Casablanca"
        )
        request = self.factory.get("core_main_set_timezone")
        request.user = self.user1

        # Act
        response = set_timezone(request)

        # Assert
        self.assertTrue("form" in response.content.decode())
        self.assertTrue(
            '<option value="Africa/Casablanca" selected>Africa/Casablanca</option>'
            in response.content.decode()
        )

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    @patch("core_main_app.components.user_preferences.api.upsert")
    def test_post_update_redirects(self, mock_upsert, mock_get_by_user):
        """test_post_update_redirects

        Args:
            mock_get_by_user:
            mock_upsert:

        Returns:

        """
        mock_get_by_user.return_value = UserPreferences(
            user_id="1", timezone="GMT"
        )
        mock_upsert.return_value = UserPreferences(user_id="1", timezone="UTC")

        # Arrange
        request = self.factory.post("core_main_set_timezone")
        request.POST = {"timezone": "UTC"}
        request.user = self.user1
        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)

        # Act
        response = set_timezone(request)

        # Assert
        self.assertEqual(response.status_code, 302)

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    @patch("core_main_app.components.user_preferences.api.upsert")
    def test_post_new_redirects(self, mock_upsert, mock_get_by_user):
        """test_post_new_redirects

        Args:
            mock_get_by_user:
            mock_upsert:

        Returns:

        """
        mock_get_by_user.side_effect = DoesNotExist("error")
        mock_upsert.return_value = UserPreferences(user_id="1", timezone="UTC")

        # Arrange
        request = self.factory.post("core_main_set_timezone")
        request.POST = {"timezone": "UTC"}
        request.user = self.user1
        # Add middlewares
        mock_get_response = MagicMock()
        middleware = SessionMiddleware(mock_get_response)
        middleware.process_request(request)

        # Act
        response = set_timezone(request)

        # Assert
        self.assertEqual(response.status_code, 302)

    @patch("core_main_app.components.user_preferences.api.get_by_user")
    def test_get_acl_error_returns_error(self, mock_get_by_user):
        # Arrange
        mock_get_by_user.side_effect = AccessControlError("error")
        request = self.factory.post("core_main_set_timezone")
        request.user = create_mock_user("1")

        # Act
        response = set_timezone(request)

        # Assert
        self.assertTrue("Access Forbidden" in response.content.decode())


class TestDefaultCustomLogin(SimpleTestCase):
    """TestDefaultCustomLogin"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.connected_user = create_mock_user(user_id="1")
        self.inactive_user = create_mock_user(user_id=None, is_active=False)

    @override_settings(INSTALLED_APPS=["core_main_app"])
    @patch("core_main_app.components.web_page_login.api.get")
    def test_get_returns_login_form_and_forget_password_button(
        self, mock_web_page_login_get
    ):
        """test_post_inactive_user_shows_form_with_error

        Returns:

        """
        # Arrange
        request = self.factory.get("core_main_app_login")
        request.user = self.anonymous_user
        mock_web_page_login_get.return_value = None

        # Act
        response = custom_login(request)

        # Assert
        self.assertTrue("form" in response.content.decode())
        self.assertTrue("Forgot password" in response.content.decode())

    @override_settings(INSTALLED_APPS=["core_main_app"])
    @patch("core_main_app.components.web_page_login.api.get")
    @patch("django.contrib.auth.authenticate")
    @patch("django.contrib.auth.login")
    def test_post_inactive_user_shows_form_with_error(
        self,
        mock_login,
        mock_authenticate,
        mock_web_page_login_get,
    ):
        """test_post_inactive_user_shows_form_with_error

        Returns:

        """
        # Arrange
        request = self.factory.post("core_main_app_login")
        request.method = "POST"
        request.POST = {
            "username": "user",
            "password": "pass",
            "next_page": None,
        }
        request.user = self.inactive_user
        mock_web_page_login_get.return_value = None
        mock_authenticate.return_value = self.inactive_user
        mock_login.return_value = None

        # Act
        response = custom_login(request)

        # Assert
        self.assertTrue("form" in response.content.decode())
        self.assertTrue(
            "Your username is not activated yet." in response.content.decode()
        )

    @override_settings(INSTALLED_APPS=["core_main_app"])
    @patch("core_main_app.components.web_page_login.api.get")
    @patch("django.contrib.auth.authenticate")
    @patch("django.contrib.auth.login")
    def test_post_active_user_redirects_to_page(
        self,
        mock_login,
        mock_authenticate,
        mock_web_page_login_get,
    ):
        """test_post_inactive_user_shows_form_with_error

        Returns:

        """
        # Arrange
        request = self.factory.post("core_main_app_login")
        request.method = "POST"
        request.POST = {
            "username": "user",
            "password": "pass",
            "next_page": None,
        }
        request.user = self.inactive_user
        mock_web_page_login_get.return_value = None
        mock_authenticate.return_value = self.connected_user
        mock_login.return_value = None

        # Act
        response = custom_login(request)

        # Assert
        self.assertTrue(response.status_code, 302)

    @override_settings(INSTALLED_APPS=["core_main_app"])
    @patch("core_main_app.components.web_page_login.api.get")
    @patch("django.contrib.auth.authenticate")
    @patch("django.contrib.auth.login")
    def test_post_with_error_renders_login_page_with_errors(
        self,
        mock_login,
        mock_authenticate,
        mock_web_page_login_get,
    ):
        """test_post_inactive_user_shows_form_with_error

        Returns:

        """
        # Arrange
        request = self.factory.post("core_main_app_login")
        request.method = "POST"
        request.POST = {
            "username": "user",
            "password": "pass",
            "next_page": None,
        }
        request.user = self.inactive_user
        mock_web_page_login_get.return_value = None
        mock_authenticate.return_value = self.connected_user
        mock_login.side_effect = Exception()

        # Act
        response = custom_login(request)

        # Assert
        self.assertTrue("form" in response.content.decode())
        self.assertTrue(
            "Invalid username and/or password." in response.content.decode()
        )


class TestCustomLogout(SimpleTestCase):
    """TestCustomLogout"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.connected_user = create_mock_user(user_id="1")

    @override_settings(INSTALLED_APPS=["core_main_app"])
    @patch("django.contrib.auth.logout")
    def test_logout_redirects(self, mock_logout):
        """test_logout_redirects

        Returns:

        """
        # Arrange
        request = self.factory.get("core_main_app_logout")
        request.user = self.connected_user
        mock_logout.return_value = None

        # Act
        response = custom_logout(request)

        # Assert
        self.assertTrue(response.status_code, 302)


class TestXmlEditor(SimpleTestCase):
    """Test Xml Editor"""

    @patch.multiple(XmlEditor, __abstractmethods__=set())
    @patch.object(xml, "format_content_xml")
    def test_get_context_calls_format_content_xml_when_content_is_not_empty(
        self, mock_format_content_xml
    ):
        """test_get_context_calls_format_content_xml_when_content_is_not_empty

        Returns:

        """
        # Arrange
        data = Data(template=Template())

        # Act
        XmlEditor().get_context(data, "title1", "<root>test</root>")

        # Assert
        mock_format_content_xml.assert_called()

    @patch.multiple(XmlEditor, __abstractmethods__=set())
    @patch.object(xml, "format_content_xml")
    def test_get_context_with_empty_content(self, mock_format_content_xml):
        """test_get_context_with_empty_content

        Returns:

        """
        # Arrange
        data = Data(template=Template())

        # Act
        XmlEditor().get_context(data, "title1", "")

        # Assert
        mock_format_content_xml.assert_not_called()


class TestJSONEditor(SimpleTestCase):
    """Test JSON Editor"""

    @patch.multiple(JSONEditor, __abstractmethods__=set())
    def test_get_context_json_editor_returns_context(
        self,
    ):
        """test_get_context_calls_format_content_json_when_content_is_not_empty

        Returns:

        """
        # Arrange
        data = Data(template=Template())

        # Act
        context = JSONEditor().get_context(
            data, "title1", '{"name": "curator"}'
        )

        # Assert
        self.assertEqual(context["document_name"], "Data")
        self.assertEqual(context["template_id"], None)
