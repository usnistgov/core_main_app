""" Blob utils test class
"""
import unittest
from unittest import TestCase
from unittest.mock import patch

from django.conf import settings

from core_main_app.commons.exceptions import BlobDownloaderUrlParseError
from core_main_app.utils.blob_downloader import BlobDownloader
from tests.test_settings import SERVER_URI


class TestBlobDownloaderIsUrlFormLocalInstance(TestCase):
    """Test BlobDownloader with local instance"""

    def test_is_url_from_local_instance_returns_false_if_url_is_not_from_local_instance(
        self,
    ):
        """test is url from local instance returns false if url is not from local instance

        Returns:

        """
        # Arrange / Act
        return_value = BlobDownloader(
            "http://google.com"
        ).is_url_from_local_instance()
        # Assert
        self.assertEqual(return_value, False)

    def test_is_url_from_local_instance_returns_true_if_url_is_from_local_instance(
        self,
    ):
        """test is url from local instance returns true if url is from local instance

        Returns:

        """
        # Arrange / Act
        return_value = BlobDownloader(
            f"{settings.SERVER_URI}/987653456789"
        ).is_url_from_local_instance()
        # Assert
        self.assertEqual(return_value, True)


class TestBlobDownloaderGetUrlBase(TestCase):
    """Test BlobDownloader.get_url_base"""

    def test_get_url_base_returns_url_base(self):
        """test get url base returns url base

        Returns:

        """
        # Arrange / Act
        return_value = BlobDownloader(
            f"{settings.SERVER_URI}/987653456789"
        ).get_url_base()
        # Assert
        self.assertEqual(return_value, SERVER_URI)

    def test_get_url_base_raise_exception_if_url_cannot_be_parsed(self):
        """test get url base raise exception if url cannot be parsed

        Returns:

        """
        # Assert
        with self.assertRaises(BlobDownloaderUrlParseError):
            # Arrange / Act
            BlobDownloader("random_string").get_url_base()


class TestBlobDownloaderGetBlobResponse(TestCase):
    """Test BlobDownloader.get_blob_response"""

    def test_get_blob_response_raise_exception_if_url_is_unidentified(self):
        """test get blob response raise exception if url is unidentified

        Returns:

        """
        # Assert
        with self.assertRaises(BlobDownloaderUrlParseError):
            # Arrange / Act
            BlobDownloader("random_string").get_blob_response()

    @patch(
        "core_main_app.utils.requests_utils.requests_utils.send_get_request"
    )
    def test_get_blob_response_return_blob_from_local_if_url_is_local(
        self, mock_send_get_request
    ):
        """test get blob response return blob from local if url is local

        Args:
            mock_send_get_request:

        Returns:

        """
        # Arrange / Act
        mock_send_get_request.return_value = "local"
        return_value = BlobDownloader(
            f"{settings.SERVER_URI}/987653456789"
        ).get_blob_response()
        # Assert
        self.assertEqual(return_value, "local")

    @unittest.skip("How to mock the import done in the API?")
    @patch(
        "core_federated_search_app.components.instance.api.get_blob_response_from_url"
    )
    def test_get_blob_response_return_blob_from_remote_if_url_is_identified_as_remote_federated(
        self, mock_send_get_request
    ):
        """test get blob response return blob from remote if url is identified as remote federated

        Args:
            mock_send_get_request:

        Returns:

        """
        # Arrange / Act
        mock_send_get_request.return_value = "remote"
        with patch.object(
            settings, "INSTALLED_APPS", ["core_federated_search_app"]
        ):
            return_value = BlobDownloader(
                "http://my.remote.com/987653456789"
            ).get_blob_response()
        # Assert
        self.assertEqual(return_value, "remote")
