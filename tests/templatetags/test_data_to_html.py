""" Unit tests of data_to_html templatetag
"""

from unittest.case import TestCase
from unittest.mock import patch, MagicMock

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.templatetags.data_to_html import (
    data_detail_html,
    _get_template_html_rendering,
)


class TestDataToHtml(TestCase):
    """TestDataToHtml"""

    def test_data_detail_html_with_none_returns_none(self):
        """test_data_detail_html_with_none_returns_none

        Returns:

        """
        result = data_detail_html(None)
        self.assertIsNone(result)

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_data_detail_html_without_template_html_rendering_returns_none(
        self, mock_get_by_template_id
    ):
        """test_data_detail_html_without_template_html_rendering_returns_none

        Returns:

        """
        mock_get_by_template_id.side_effect = DoesNotExist("Error")
        mock_data = {
            "content": {"value": "test"},
            "template": {"format": "JSON", "id": 1},
        }
        result = data_detail_html(mock_data)
        self.assertIsNone(result)

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_data_detail_html_without_detail_rendering_returns_none(
        self, mock_get_by_template_id
    ):
        """test_data_detail_html_without_detail_rendering_returns_none

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.detail_rendering = None
        mock_get_by_template_id.return_value = mock_template_html_rendering
        mock_data = {
            "content": {"value": "test"},
            "template": {"format": "JSON", "id": 1},
        }
        result = data_detail_html(mock_data)
        self.assertIsNone(result)

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_data_detail_html_with_dict_returns_html(
        self, mock_get_by_template_id
    ):
        """test_data_detail_html_with_dict_returns_html

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.detail_rendering = (
            "{{dict_content.value}}"
        )
        mock_get_by_template_id.return_value = mock_template_html_rendering
        mock_data = {
            "content": {"value": "test"},
            "template": {"format": "JSON", "id": 1},
        }
        result = data_detail_html(mock_data)
        self.assertEqual(result, "test")

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_data_detail_html_with_string_dict_returns_html(
        self, mock_get_by_template_id
    ):
        """test_data_detail_html_with_dict_returns_html

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.detail_rendering = (
            "{{dict_content.value}}"
        )
        mock_get_by_template_id.return_value = mock_template_html_rendering
        mock_data = {
            "content": '{"value": "test"}',
            "template": {"format": "JSON", "id": 1},
        }
        result = data_detail_html(mock_data)
        self.assertEqual(result, "test")

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_data_detail_html_with_xml_returns_html(
        self, mock_get_by_template_id
    ):
        """test_data_detail_html_with_xml_returns_html

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.detail_rendering = (
            "{{dict_content.value}}"
        )
        mock_get_by_template_id.return_value = mock_template_html_rendering
        mock_data = {
            "content": "<value>test</value>",
            "template": {"format": "XSD", "id": 1},
        }
        result = data_detail_html(mock_data)
        self.assertEqual(result, "test")

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_data_detail_html_with_unknown_format_returns_none(
        self, mock_get_by_template_id
    ):
        """test_data_detail_html_with_unknown_format_returns_none

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.detail_rendering = (
            "{{dict_content.value}}"
        )
        mock_get_by_template_id.return_value = mock_template_html_rendering
        mock_data = {
            "content": "value: test",
            "template": {"format": "YAML", "id": 1},
        }
        result = data_detail_html(mock_data)
        self.assertIsNone(result)

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_hash"
    )
    def test_data_detail_html_get_by_hash_with_dict_returns_html(
        self, mock_get_by_template_hash
    ):
        """test_data_detail_html_get_by_hash_with_dict_returns_html

        Returns:

        """
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.detail_rendering = (
            "{{dict_content.value}}"
        )
        mock_get_by_template_hash.return_value = mock_template_html_rendering
        mock_data = {
            "content": {"value": "test"},
            "template": {"format": "JSON", "hash": "abcd"},
        }
        result = data_detail_html(mock_data)
        self.assertEqual(result, "test")

    def test_data_detail_html_returns_none_if_id_or_hash_missing(
        self,
    ):
        """test_data_detail_html_returns_none_if_id_or_hash_missing

        Returns:

        """
        mock_data = {
            "content": {"value": "test"},
            "template": {"format": "JSON"},
        }
        result = data_detail_html(mock_data)
        self.assertIsNone(result)


class TestGetTemplateHtmlRendering(TestCase):
    """TestGetTemplateHtmlRendering"""

    def setUp(self):
        """setup

        Returns:

        """
        self.detail_rendering = "detail"
        self.list_rendering = "list"

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_get_detail_template_html_rendering_return_detail_rendering(
        self, mock_get_by_template_id
    ):
        """test_get_detail_template_html_rendering_return_detail_rendering

        Returns:

        """
        # Arrange
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.detail_rendering = self.detail_rendering
        mock_template_html_rendering.list_rendering = self.list_rendering
        mock_get_by_template_id.return_value = mock_template_html_rendering

        # Act
        rendering = _get_template_html_rendering(
            template_id=1, rendering_type="detail"
        )

        # Assert
        self.assertEqual(rendering, self.detail_rendering)

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_get_list_template_html_rendering_return_list_rendering(
        self, mock_get_by_template_id
    ):
        """test_get_list_template_html_rendering_return_list_rendering

        Returns:

        """
        # Arrange
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.detail_rendering = self.detail_rendering
        mock_template_html_rendering.list_rendering = self.list_rendering
        mock_get_by_template_id.return_value = mock_template_html_rendering

        # Act
        rendering = _get_template_html_rendering(
            template_id=1, rendering_type="list"
        )

        # Assert
        self.assertEqual(rendering, self.list_rendering)

    @patch(
        "core_main_app.components.template_html_rendering.api.get_by_template_id"
    )
    def test_get_unknown_template_html_rendering_return_none(
        self, mock_get_by_template_id
    ):
        """test_get_unknown_template_html_rendering_return_none

        Returns:

        """
        # Arrange
        mock_template_html_rendering = MagicMock()
        mock_template_html_rendering.detail_rendering = self.detail_rendering
        mock_template_html_rendering.list_rendering = self.list_rendering
        mock_get_by_template_id.return_value = mock_template_html_rendering

        # Act
        rendering = _get_template_html_rendering(
            template_id=1, rendering_type="unknown"
        )

        # Assert
        self.assertEqual(rendering, None)
