""" Unit tests of format json  templatetag
"""
import json
from unittest.case import TestCase

from core_main_app.templatetags import format_json


class TestFormatJSON(TestCase):
    """Test Format JSON"""

    def test_format_json_returns_string(self):
        """test_format_json_returns_string

        Returns:

        """
        expected_value = json.dumps((json.loads('{"test": true}')), indent=8)
        result = format_json.render_json_as_html_detail('{"test": true}')
        self.assertEqual(result, expected_value)
