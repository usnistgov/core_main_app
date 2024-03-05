""" Unit test for `views.admin.ajax` package.
"""

from django.test import SimpleTestCase

from core_main_app.views.admin import ajax as admin_ajax


class TestGetXSDContentFromHTML(SimpleTestCase):
    """Test _get_xsd_content_from_html"""

    def test_get_xsd_content_from_html_returns_unescaped_string(self):
        """test_get_xsd_content_from_html_returns_unescaped_string

        Returns:

        """
        escaped_string = "&lt;xsd:schema&gt;&lt;/xsd:schema&gt;"
        expected_string = "<xsd:schema></xsd:schema>"
        self.assertEqual(
            admin_ajax._get_xsd_content_from_html(escaped_string),
            expected_string,
        )
