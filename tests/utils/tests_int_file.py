""" Blob utils test class
"""
from unittest import TestCase

from mock import patch

from core_main_app.commons.exceptions import CoreError
from core_main_app.utils.file import get_base_64_content_from_response


class TestFileUtilsGetBase64ContentFromResponse(TestCase):
    """TestFileUtilsGetBase64ContentFromResponse"""

    def test_get_base_64_content_from_response_return_base_64_encoded_string(self):
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
