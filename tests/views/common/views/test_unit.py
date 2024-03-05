""" Unit tests for `core_main_app.views.common.views` package.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.test import RequestFactory, SimpleTestCase, override_settings

from core_main_app.commons.exceptions import JSONError
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.utils import xml
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.views.common import views as common_views


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
        response = common_views.DataXMLEditor.as_view()(request)

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
        response = common_views.DataXMLEditor.as_view()(request)
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
        response = common_views.DataXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            b"The Curate App needs to be installed to use this feature.",
        )


class TestXmlEditor(SimpleTestCase):
    """Test Xml Editor"""

    @patch.multiple(common_views.XmlEditor, __abstractmethods__=set())
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
        common_views.XmlEditor().get_context(
            data, "title1", "<root>test</root>"
        )

        # Assert
        mock_format_content_xml.assert_called()

    @patch.multiple(common_views.XmlEditor, __abstractmethods__=set())
    def test_get_context_when_content_is_not_well_formed(self):
        """test_get_context_when_content_is_not_well_formed

        Returns:

        """
        # Arrange
        data = Data(template=Template())

        # Act
        result = common_views.XmlEditor().get_context(data, "title1", "<test")

        # Assert
        self.assertEquals(result["content"], "<test")


class TestJSONEditor(SimpleTestCase):
    """Test JSON Editor"""

    @patch.multiple(common_views.JSONEditor, __abstractmethods__=set())
    def test_get_context_json_editor_returns_context(
        self,
    ):
        """test_get_context_calls_format_content_json_when_content_is_not_empty

        Returns:

        """
        # Arrange
        data = Data(template=Template())

        # Act
        context = common_views.JSONEditor().get_context(
            data, "title1", '{"name": "curator"}'
        )

        # Assert
        self.assertEqual(context["document_name"], "Data")
        self.assertEqual(context["template_id"], None)


class TestJSONEditorValidate(TestCase):
    """Unit tests for `JSONEditor.validate` package."""

    def setUp(self):
        """setUp"""
        self.request_factory = RequestFactory()

        with patch.multiple(
            common_views.JSONEditor, __abstractmethods__=set()
        ):
            self.editor = common_views.JSONEditor()

    def test_no_content_raises_exception(self):
        """test_no_content_raises_exception"""
        self.editor.request = self.request_factory.post("mock_path", data={})

        with self.assertRaises(Exception):
            self.editor.validate()

    def test_no_template_id_returns_400(self):
        """test_no_template_id_raises_exception"""
        self.editor.request = self.request_factory.post(
            "mock_path", data={"content": "{}"}
        )

        self.assertTrue(self.editor.validate().status_code, 400)

    @patch.object(common_views, "template_api")
    def test_template_get_by_id_called(self, mock_template_api):
        """test_template_get_by_id_called"""
        mock_template_id = "0"
        self.editor.request = self.request_factory.post(
            "mock_path",
            data={"content": "{}", "template_id": mock_template_id},
        )

        self.editor.validate()

        mock_template_api.get_by_id.assert_called_with(
            mock_template_id, self.editor.request
        )

    @patch.object(common_views, "template_api")
    def test_template_get_by_id_error_returns_400(self, mock_template_api):
        """test_template_get_by_id_error_returns_400"""
        mock_template_api.get_by_id.side_effect = Exception(
            "mock_template_api_get_by_id_exception"
        )
        self.editor.request = self.request_factory.post(
            "mock_path", data={"content": "{}", "template_id": 0}
        )

        self.assertTrue(self.editor.validate().status_code, 400)

    @patch.object(common_views, "validate_json_data")
    @patch.object(common_views, "template_api")
    def test_validate_json_data_called(
        self, mock_template_api, mock_validate_json_data
    ):
        """test_validate_json_data_called"""
        mock_template = MagicMock()
        mock_content = "{}"

        mock_template_api.get_by_id.return_value = mock_template
        self.editor.request = self.request_factory.post(
            "mock_path", data={"content": mock_content, "template_id": 0}
        )

        self.editor.validate()

        mock_validate_json_data.assert_called_with(
            mock_content, mock_template.content
        )

    @patch.object(common_views, "validate_json_data")
    @patch.object(common_views, "template_api")
    def test_validate_json_data_json_error_returns_400(
        self, mock_template_api, mock_validate_json_data
    ):
        """test_validate_json_data_json_error_returns_400"""
        mock_template = MagicMock()
        mock_content = "{}"

        mock_template_api.get_by_id.return_value = mock_template
        mock_validate_json_data.side_effect = JSONError(["error1", "error2"])
        self.editor.request = self.request_factory.post(
            "mock_path", data={"content": mock_content, "template_id": 0}
        )

        self.assertEqual(self.editor.validate().status_code, 400)

    @patch.object(common_views, "validate_json_data")
    @patch.object(common_views, "template_api")
    def test_validate_json_data_exception_raises_json_error(
        self, mock_template_api, mock_validate_json_data
    ):
        """test_validate_json_data_json_error_returns_400"""
        mock_template = MagicMock()
        mock_content = "{}"

        mock_template_api.get_by_id.return_value = mock_template
        mock_validate_json_data.side_effect = Exception("mock_exception")
        self.editor.request = self.request_factory.post(
            "mock_path", data={"content": mock_content, "template_id": 0}
        )

        with self.assertRaises(JSONError):
            self.editor.validate()

    @patch.object(common_views, "validate_json_data")
    @patch.object(common_views, "template_api")
    def test_validate_json_data_success_returns_200(
        self, mock_template_api, mock_validate_json_data
    ):
        """test_validate_json_data_json_error_returns_400"""
        mock_template = MagicMock()
        mock_content = "{}"

        mock_template_api.get_by_id.return_value = mock_template
        mock_validate_json_data.return_value = None
        self.editor.request = self.request_factory.post(
            "mock_path", data={"content": mock_content, "template_id": 0}
        )

        self.assertEqual(self.editor.validate().status_code, 200)
