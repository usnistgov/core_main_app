""" Blob utils test class
"""
import unittest
from unittest import TestCase

import mock
from django.conf import settings
from mock import patch

from core_main_app.commons.exceptions import BlobDownloaderUrlParseError
from core_main_app.utils.blob_downloader import BlobDownloader
from tests.test_settings import SERVER_URI


class TestBlobDownloaderIsUrlFormLocalInstance(TestCase):
    def test_is_url_from_local_instance_returns_false_if_url_is_not_from_local_instance(
        self,
    ):
        # Arrange / Act
        return_value = BlobDownloader("http://google.com").is_url_from_local_instance()
        # Assert
        self.assertEqual(return_value, False)

    def test_is_url_from_local_instance_returns_true_if_url_is_from_local_instance(
        self,
    ):
        # Arrange / Act
        return_value = BlobDownloader(
            "http://example.com/987653456789"
        ).is_url_from_local_instance()
        # Assert
        self.assertEqual(return_value, True)


class TestBlobDownloaderGetUrlBase(TestCase):
    def test_get_url_base_returns_url_base(self):
        # Arrange / Act
        return_value = BlobDownloader("http://example.com/987653456789").get_url_base()
        # Assert
        self.assertEqual(return_value, SERVER_URI)

    def test_get_url_base_raise_exception_if_url_is_not_parsable(self):
        # Assert
        with self.assertRaises(BlobDownloaderUrlParseError):
            # Arrange / Act
            BlobDownloader("random_string").get_url_base()


class TestBlobDownloaderGetBlobResponse(TestCase):
    def test_get_blob_response_raise_exception_if_url_is_unidentified(self):
        # Assert
        with self.assertRaises(BlobDownloaderUrlParseError):
            # Arrange / Act
            BlobDownloader("random_string").get_blob_response()

    @patch("core_main_app.utils.requests_utils.requests_utils.send_get_request")
    def test_get_blob_response_return_blob_from_local_if_url_is_local(
        self, mock_send_get_request
    ):
        # Arrange / Act
        mock_send_get_request.return_value = "local"
        return_value = BlobDownloader(
            "http://example.com/987653456789"
        ).get_blob_response()
        # Assert
        self.assertEqual(return_value, "local")

    @unittest.skip("How to mock the import done in the API?")
    @patch(
        "core_federated_search_app.components.instance.api.get_blob_response_from_url"
    )
    def test_get_blob_response_return_blob_from_federated_remote_if_url_is_identified_as_remote_federated(
        self, mock_send_get_request
    ):
        # Arrange / Act
        mock_send_get_request.return_value = "remote"
        with mock.patch.object(
            settings, "INSTALLED_APPS", ["core_federated_search_app"]
        ):
            return_value = BlobDownloader(
                "http://my.remote.com/987653456789"
            ).get_blob_response()
        # Assert
        self.assertEqual(return_value, "remote")
