"""Requests utils tests"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_main_app.settings import SSL_CERTIFICATES_DIR
from core_main_app.utils.requests_utils.requests_utils import (
    send_get_request,
    send_post_request,
    send_put_request,
    send_delete_request,
)


class TestSendGetRequest(TestCase):
    """Test send_get_request"""

    @patch("core_main_app.utils.requests_utils.requests_utils.requests.get")
    def test_send_get_request_calls_validate_and_sets_verify_default(
        self, mock_get
    ):
        """test send get request calls validate and sets verify default"""
        mock_response = MagicMock()
        mock_get.return_value = mock_response

        url = "https://example.com/api"
        resp = send_get_request(url)

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], url)
        self.assertEqual(kwargs.get("verify"), SSL_CERTIFICATES_DIR)
        self.assertEqual(resp, mock_response)

    @patch("core_main_app.utils.requests_utils.requests_utils.requests.get")
    def test_send_get_request_passes_verify_if_provided(self, mock_get):
        """test send get request passes verify if provided"""
        mock_get.return_value = MagicMock()

        url = "https://example.com/api"
        send_get_request(url, verify="/custom/ca")

        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs.get("verify"), "/custom/ca")


class TestSendPostRequest(TestCase):
    """Test send_post_request"""

    @patch("core_main_app.utils.requests_utils.requests_utils.requests.post")
    def test_send_post_request_calls_validate_and_sets_verify_default(
        self, mock_post
    ):
        """test send post request calls validate and sets verify default"""
        mock_response = MagicMock()
        mock_post.return_value = mock_response

        url = "https://example.com/api"
        resp = send_post_request(url, data={"a": 1})

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], url)
        self.assertEqual(kwargs.get("verify"), SSL_CERTIFICATES_DIR)
        self.assertEqual(resp, mock_response)

    @patch("core_main_app.utils.requests_utils.requests_utils.requests.post")
    def test_send_post_request_passes_verify_if_provided(self, mock_post):
        """test send post request passes verify if provided"""
        mock_post.return_value = MagicMock()
        url = "https://example.com/api"
        send_post_request(url, data={"a": 1}, verify="/custom/ca")
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs.get("verify"), "/custom/ca")


class TestSendPutRequest(TestCase):
    """Test send_put_request"""

    @patch("core_main_app.utils.requests_utils.requests_utils.requests.put")
    def test_send_put_request_calls_validate_and_sets_verify_default(
        self, mock_put
    ):
        """test send put request calls validate and sets verify default"""
        mock_response = MagicMock()
        mock_put.return_value = mock_response

        url = "https://example.com/api"
        resp = send_put_request(url, data={"a": 1})

        mock_put.assert_called_once()
        args, kwargs = mock_put.call_args
        self.assertEqual(args[0], url)
        self.assertEqual(kwargs.get("verify"), SSL_CERTIFICATES_DIR)
        self.assertEqual(resp, mock_response)

    @patch("core_main_app.utils.requests_utils.requests_utils.requests.put")
    def test_send_put_request_passes_verify_if_provided(self, mock_put):
        """test send put request passes verify if provided"""
        mock_put.return_value = MagicMock()
        url = "https://example.com/api"
        send_put_request(url, data={"a": 1}, verify="/custom/ca")
        args, kwargs = mock_put.call_args
        self.assertEqual(kwargs.get("verify"), "/custom/ca")


class TestSendDeleteRequest(TestCase):
    """Test send_delete_request"""

    @patch("core_main_app.utils.requests_utils.requests_utils.requests.delete")
    def test_send_delete_request_calls_validate_and_sets_verify_default(
        self, mock_delete
    ):
        """test send delete request calls validate and sets verify default"""
        mock_response = MagicMock()
        mock_delete.return_value = mock_response

        url = "https://example.com/api"
        resp = send_delete_request(url)

        mock_delete.assert_called_once()
        args, kwargs = mock_delete.call_args
        self.assertEqual(args[0], url)
        self.assertEqual(kwargs.get("verify"), SSL_CERTIFICATES_DIR)
        self.assertEqual(resp, mock_response)

    @patch("core_main_app.utils.requests_utils.requests_utils.requests.delete")
    def test_send_delete_request_passes_verify_if_provided(self, mock_delete):
        """test send delete request passes verify if provided"""
        mock_delete.return_value = MagicMock()
        url = "https://example.com/api"
        send_delete_request(url, verify="/custom/ca")
        args, kwargs = mock_delete.call_args
        self.assertEqual(kwargs.get("verify"), "/custom/ca")
