"""Blob utils test class"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_main_app.commons.exceptions import CoreError
from core_main_app.components.template.models import Template
from core_main_app.utils.file import (
    get_base_64_content_from_response,
    get_byte_size_from_string,
    get_file_extension,
    get_data_file_content_type_for_template_format,
    get_template_file_content_type_for_template_format,
    get_data_file_extension_for_template_format,
    get_template_file_extension_for_template_format,
    get_file_http_response,
    get_filename_from_response,
)
from urllib.parse import quote


class TestFileUtilsGetBase64ContentFromResponse(TestCase):
    """TestFileUtilsGetBase64ContentFromResponse"""

    def test_get_base_64_content_from_response_return_base_64_encoded_string(
        self,
    ):
        """test get base 64 content from response return base 64 encoded string

        Returns:

        """
        # Arrange
        response = MockResponse()
        # Act
        result = get_base_64_content_from_response(response)
        # Assert
        self.assertEqual(True, isinstance(result, str))

    def test_get_base_64_content_from_response_raise_core_exception_if_encoding_fails(
        self,
    ):
        """test get base 64 content from response raise core exception if encoding fails

        Returns:

        """
        # Arrange
        response = MockResponse()
        response.content = "this_is_a_string and it will fail"
        # Assert
        with self.assertRaises(CoreError):
            # Act
            get_base_64_content_from_response(response)

    @patch("base64.b64decode")
    def test_get_base_64_content_from_response_raise_core_exception_if_ascii_decoding_fails(
        self, mock_b64decode
    ):
        """test get base 64 content from response raise core exception if ascii decoding fails

        Args:
            mock_b64decode:

        Returns:

        """
        # Arrange
        response = MockResponse()
        response.content = "this_is_a_string and it will fail"
        mock_b64decode.side_effect = Exception()
        # Assert
        with self.assertRaises(CoreError):
            # Act
            get_base_64_content_from_response(response)


class MockResponse:
    """MockResponse"""

    content = b"my_string"


class TestGetByteSizeFromString(TestCase):
    """TestGetByteSizeFromString"""

    def test_get_byte_size_from_string_returns_int(
        self,
    ):
        """test_get_byte_size_from_string_returns_int

        Returns:

        """
        # Arrange
        result = get_byte_size_from_string("test")
        self.assertTrue(isinstance(result, int))
        self.assertTrue(result > 0)

    def test_get_byte_size_from_empty_string_returns_zero(
        self,
    ):
        """test_get_byte_size_from_string_returns_int

        Returns:

        """
        # Arrange
        result = get_byte_size_from_string("")
        self.assertTrue(result == 0)


class TestGetFileExtension(TestCase):
    """TestGetFileExtension"""

    def test_get_xml_file_extension_returns_xml(
        self,
    ):
        """test_get_xml_file_extension_returns_xml

        Returns:

        """
        result = get_file_extension("filename.xml")
        self.assertEqual(result, ".xml")

    def test_get_xsd_file_extension_returns_xsd(
        self,
    ):
        """test_get_xsd_file_extension_returns_xsd

        Returns:

        """
        result = get_file_extension("filename.xsd")
        self.assertEqual(result, ".xsd")

    def test_get_json_file_extension_returns_json(
        self,
    ):
        """test_get_json_file_extension_returns_json

        Returns:

        """
        result = get_file_extension("filename.json")
        self.assertEqual(result, ".json")

    def test_get_no_file_extension_returns_empty_string(
        self,
    ):
        """test_get_no_file_extension_returns_empty_string

        Returns:

        """
        result = get_file_extension("filename")
        self.assertEqual(result, "")


class TestGetFileInfoFromConstants(TestCase):
    """TestGetFileInfoFromConstants"""

    def test_get_data_file_content_type_for_template_format_returns_format_if_found(
        self,
    ):
        """test_get_data_file_content_type_for_template_format_returns_format_if_found

        Returns:

        """
        result = get_data_file_content_type_for_template_format(Template.XSD)
        self.assertEqual(result, "text/xml")

    def test_get_data_file_content_type_for_template_format_returns_none_if_not_found(
        self,
    ):
        """test_get_data_file_content_type_for_template_format_returns_none_if_not_found

        Returns:

        """
        result = get_data_file_content_type_for_template_format("BAD")
        self.assertIsNone(result)

    def test_get_template_file_content_type_for_template_format_returns_format_if_found(
        self,
    ):
        """test_get_template_file_content_type_for_template_format_returns_format_if_found

        Returns:

        """
        result = get_template_file_content_type_for_template_format(
            Template.XSD
        )
        self.assertEqual(result, "text/xml")

    def test_get_template_file_content_type_for_template_format_returns_none_if_not_found(
        self,
    ):
        """test_get_template_file_content_type_for_template_format_returns_none_if_not_found

        Returns:

        """
        result = get_template_file_content_type_for_template_format("BAD")
        self.assertIsNone(result)

    def test_get_data_file_extension_for_template_format_returns_format_if_found(
        self,
    ):
        """test_get_data_file_extension_for_template_format_returns_format_if_found

        Returns:

        """
        result = get_data_file_extension_for_template_format(Template.XSD)
        self.assertEqual(result, ".xml")

    def test_get_data_file_extension_for_template_format_returns_format_if_not_found(
        self,
    ):
        """test_get_data_file_extension_for_template_format_returns_format_if_not_found

        Returns:

        """
        result = get_data_file_extension_for_template_format("BAD")
        self.assertEqual(result, "")

    def test_get_template_file_extension_for_template_format_returns_format_if_found(
        self,
    ):
        """test_get_template_file_extension_for_template_format_returns_format_if_found

        Returns:

        """
        result = get_template_file_extension_for_template_format(Template.XSD)
        self.assertEqual(result, ".xsd")

    def test_get_template_file_extension_for_template_format_returns_format_if_not_found(
        self,
    ):
        """test_get_template_file_extension_for_template_format_returns_format_if_not_found

        Returns:

        """
        result = get_template_file_extension_for_template_format("BAD")
        self.assertEqual(result, "")


class TestGetFileHttpResponse(TestCase):
    """TestGetFileHttpResponse"""

    def test_get_file_http_response_with_xml_file(self):
        """test_get_file_http_response_with_xml_file

        Returns:

        """
        response = get_file_http_response(
            file_content="<tag></tag>", file_name="test.xml"
        )
        self.assertEqual(response.content, b"<tag></tag>")
        self.assertEqual(response.headers["Content-Type"], "application/xml")

    def test_get_file_http_response_with_json_file(self):
        """test_get_file_http_response_with_json_file

        Returns:

        """
        response = get_file_http_response(
            file_content='{"element": "value"}', file_name="test.json"
        )
        self.assertEqual(response.content, b'{"element": "value"}')
        self.assertEqual(response.headers["Content-Type"], "application/json")

    def test_get_file_http_response_with_utf8_filename(self):
        """test_get_file_http_response_with_utf8_filename"""
        filename = "tést_fîle.pdf"
        response = get_file_http_response(
            file_content="content", file_name=filename
        )
        header = response["Content-Disposition"]

        encoded_name = quote(filename)
        fallback_name = "tst_fle.pdf"
        self.assertIn(f"filename*=UTF-8''{encoded_name}", header)
        self.assertIn(f'filename="{fallback_name}"', header)

    def test_get_file_http_response_adds_extension(self):
        """test_get_file_http_response_adds_extension"""
        response = get_file_http_response(
            file_content="content", file_name="test", extension="xml"
        )
        self.assertIn('filename="test.xml"', response["Content-Disposition"])


class TestGetFilenameFromResponse(TestCase):
    """TestGetFilenameFromResponse"""

    def test_get_filename(self):
        """test_get_filename"""
        mock_response = MagicMock()
        mock_response.headers = {
            "content-disposition": 'attachment; filename="test.txt"'
        }

        self.assertEqual(get_filename_from_response(mock_response), "test.txt")

    def test_get_filename_utf8_encoded(self):
        """test_get_filename_utf8_encoded"""
        filename = "tést_fîle.pdf"
        encoded_filename = quote(filename)
        fallback_name = "tst_fle.pdf"
        headers = f"attachment; filename='{fallback_name}'; filename*=UTF-8''{encoded_filename}"
        mock_response = MagicMock()
        mock_response.headers = {"content-disposition": headers}

        self.assertEqual(get_filename_from_response(mock_response), filename)

    def test_get_filename_fallback_only(self):
        """test_get_filename_fallback_only"""
        filename = "filename.pdf"

        mock_response = MagicMock()
        mock_response.headers = {
            "content-disposition": f"attachment; filename='{filename}'"
        }

        self.assertEqual(get_filename_from_response(mock_response), filename)

    def test_get_filename_no_header(self):
        """test_get_filename_no_header"""
        mock_response = MagicMock()
        mock_response.headers = {}

        self.assertIsNone(get_filename_from_response(mock_response))

    def test_get_filename_invalid_header(self):
        """test_get_filename_invalid_header"""
        mock_response = MagicMock()
        mock_response.headers = {
            "content-disposition": "attachment; size=1234"
        }

        self.assertIsNone(get_filename_from_response(mock_response))
