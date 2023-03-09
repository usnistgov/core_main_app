""" Unit test views
"""
from unittest.mock import patch, MagicMock

from django.test import RequestFactory, SimpleTestCase, override_settings

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.views.common.views import DataContentEditor


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
        response = DataContentEditor.as_view()(request)

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
        response = DataContentEditor.as_view()(request)
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
        response = DataContentEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            b"The Curate App needs to be installed to use this feature.",
        )
