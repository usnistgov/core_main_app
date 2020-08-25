"""BLOB component utils
"""
from django.urls import reverse

from core_main_app.settings import SERVER_URI


def get_blob_download_uri(blob, request):
    """Return download url for the blob.

    Args:
        blob:
        request:

    Returns:

    """
    # get URI to download blob
    blob_download_uri = SERVER_URI + reverse(
        "core_main_app_rest_blob_download", kwargs={"pk": str(blob.id)}
    )

    return blob_download_uri
