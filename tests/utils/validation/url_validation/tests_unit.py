"""URL validation utils tests"""

import ipaddress
from unittest import TestCase
from unittest.mock import patch

from django.core.exceptions import ValidationError

from core_main_app.utils.validation.url_validation import (
    is_same_origin,
    validate_request_url,
)


class TestIsSameOrigin(TestCase):
    """Test is_same_origin"""

    @patch(
        "core_main_app.utils.validation.url_validation.settings.SERVER_URI",
        "http://127.0.0.1:8000",
    )
    def test_is_same_origin_returns_true_when_origin_matches_server(self):
        """test is same origin returns true when origin matches server"""
        url = "http://127.0.0.1:8000/rest/data/"
        self.assertTrue(is_same_origin(url))

    @patch(
        "core_main_app.utils.validation.url_validation.settings.SERVER_URI",
        "http://127.0.0.1:8000",
    )
    def test_is_same_origin_returns_false_when_origin_differs(self):
        """test is same origin returns false when origin differs"""
        url = "https://example.com/rest/data/"
        self.assertFalse(is_same_origin(url))

    @patch(
        "core_main_app.utils.validation.url_validation.settings.SERVER_URI",
        "http://127.0.0.1:8000",
    )
    def test_is_same_origin_returns_false_when_url_unparsable(self):
        """test is same origin returns false when url unparsable"""
        url = "no-scheme-and-netloc"
        self.assertFalse(is_same_origin(url))

    @patch(
        "core_main_app.utils.validation.url_validation.settings.SERVER_URI",
        "http://127.0.0.1:8000",
    )
    def test_is_same_origin_returns_false_when_netloc_missing(self):
        """test is same origin returns false when netloc missing"""
        url = "http:///path"
        self.assertFalse(is_same_origin(url))


class TestValidateRequestUrl(TestCase):
    """Test validate_request_url"""

    def test_validate_request_url_passes_for_http_domain(self):
        """test validate request url passes for http domain"""
        validate_request_url("http://example.com/path")

    def test_validate_request_url_passes_for_https_domain(self):
        """test validate request url passes for https domain"""
        validate_request_url("https://example.com/path")

    def test_validate_request_url_passes_for_non_link_local_ip(self):
        """test validate request url passes for non link local ip"""
        with patch(
            "core_main_app.utils.validation.url_validation.ipaddress.ip_address"
        ) as mock_ip:
            mock_ip.return_value.is_link_local = False
            validate_request_url("http://1.2.3.4/path")

    def test_validate_request_url_raises_for_disallowed_scheme(self):
        """test validate request url raises for disallowed scheme"""
        with self.assertRaises(ValidationError):
            validate_request_url("file:///etc/passwd")

    def test_validate_request_url_raises_for_ftp_scheme(self):
        """test validate request url raises for ftp scheme"""
        with self.assertRaises(ValidationError):
            validate_request_url("ftp://example.com/")

    def test_validate_request_url_raises_for_link_local_ipv4(self):
        """test validate request url raises for link local ipv4"""
        with patch(
            "core_main_app.utils.validation.url_validation.ipaddress.ip_address"
        ) as mock_ip:
            mock_ip.return_value.is_link_local = True
            with self.assertRaises(ValidationError):
                validate_request_url("http://1.2.3.4/")

    def test_validate_request_url_raises_for_link_local_ipv6(self):
        """test validate request url raises for link local ipv6"""
        with patch(
            "core_main_app.utils.validation.url_validation.ipaddress.ip_address"
        ) as mock_ip:
            mock_ip.return_value.is_link_local = True
            with self.assertRaises(ValidationError):
                validate_request_url("http://[::1]/path")

    def test_validate_request_url_raises_for_unparsable_url(self):
        """test validate request url raises for unparsable url"""
        with self.assertRaises(ValidationError):
            validate_request_url(None)

    @patch("core_main_app.utils.validation.url_validation.urlparse")
    def test_validate_request_url_raises_on_urlparse_error(
        self, mock_urlparse
    ):
        """test validate request url raises on urlparse error"""
        mock_urlparse.side_effect = ValueError("unparsable")
        with self.assertRaises(ValidationError):
            validate_request_url("http://example.com")

    @patch(
        "core_main_app.utils.validation.url_validation.ipaddress.ip_address"
    )
    def test_validate_request_url_raises_on_ip_address_error(
        self, mock_ip_address
    ):
        """test validate request url raises on ip address error"""
        mock_ip_address.side_effect = RuntimeError("unexpected")
        with self.assertRaises(ValidationError):
            validate_request_url("http://1.2.3.4/")

    @patch(
        "core_main_app.utils.validation.url_validation.settings.BLOCK_URL_LINK_LOCAL",
        False,
    )
    @patch(
        "core_main_app.utils.validation.url_validation.ipaddress.ip_address"
    )
    def test_validate_request_url_allows_link_local_when_blocking_disabled(
        self, mock_ip
    ):
        """link-local is allowed when BLOCK_URL_LINK_LOCAL is False"""
        mock_ip.return_value.is_link_local = True
        # Should not raise
        validate_request_url("http://1.2.3.4/")

    @patch(
        "core_main_app.utils.validation.url_validation.settings.BLOCKED_IP_LIST",
        ["1.2.3.4"],
    )
    @patch(
        "core_main_app.utils.validation.url_validation.ipaddress.ip_address"
    )
    def test_validate_request_url_raises_for_blocked_ip(self, mock_ip):
        """URL with IP in BLOCKED_IP_LIST is rejected"""
        mock_ip.return_value = ipaddress.ip_address("1.2.3.4")
        with self.assertRaises(ValidationError):
            validate_request_url("http://1.2.3.4/")

    @patch(
        "core_main_app.utils.validation.url_validation.settings.BLOCKED_IP_LIST",
        ["9.9.9.9"],
    )
    def test_validate_request_url_raises_for_blocked_ip_real(self):
        """URL with real IP in BLOCKED_IP_LIST is rejected"""
        with self.assertRaises(ValidationError):
            validate_request_url("http://9.9.9.9/")

    @patch(
        "core_main_app.utils.validation.url_validation.settings.HTTP_ALLOWED_URL_SCHEMES",
        ("https",),
    )
    def test_validate_request_url_respects_custom_allowed_schemes(self):
        """Only schemes from settings are allowed"""
        # http should be rejected
        with self.assertRaises(ValidationError):
            validate_request_url("http://example.com/")
        # https should pass
        validate_request_url("https://example.com/")
