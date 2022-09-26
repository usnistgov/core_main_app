""" Blobs downloader utils
"""
from logging import getLogger
from urllib.parse import urlparse

from django.conf import settings

from core_main_app.commons import exceptions
from core_main_app.settings import SERVER_URI
from core_main_app.utils.requests_utils import requests_utils

logger = getLogger(__name__)


class BlobDownloader:
    """Blob Downloader Class"""

    def __init__(self, url, session_key=""):
        """Blob Downloader Constructor

        Args:
            url: blob's url
            session_key: session key if needed
        """
        self.url = url
        self.url_base = self.get_url_base()
        self.session_key = session_key

    def get_blob_response(self):
        """get the blob response from local or remote instance

        Returns: Http Response

        """
        if self.is_url_from_local_instance():
            # call the local instance giving sessionid through the call
            return requests_utils.send_get_request(
                url=self.url, cookies={"sessionid": self.session_key}
            )
        # so it can be from a federated instance
        if "core_federated_search_app" in settings.INSTALLED_APPS:
            # import the api where we need to
            import core_federated_search_app.components.instance.api as instance_api

            try:
                return instance_api.get_blob_response_from_url(
                    self.url_base, self.url
                )
            except exceptions.DoesNotExist:
                logger.info(
                    "BlobDownloader: The blob's url is not a known source"
                )
        else:
            logger.info(
                "BlobDownloader: core_federated_search_app is required"
            )

        # here is the case where the blob come from an unidentified source
        raise exceptions.BlobDownloaderError("Blob can't be downloaded")

    def is_url_from_local_instance(self):
        """is the url from a local instance or not

        Returns: Boolean

        """
        return self.url_base in SERVER_URI

    def get_url_base(self):
        """get the url base

        Returns: String

        """
        parsed_uri = urlparse(self.url)
        if not parsed_uri.scheme or not parsed_uri.netloc:
            raise exceptions.BlobDownloaderUrlParseError(
                "the url given is not parsable"
            )
        return "{uri.scheme}://{uri.netloc}".format(uri=parsed_uri)
