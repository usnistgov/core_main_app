"""BLOB component utils
"""
from django.core.urlresolvers import reverse


def get_blob_download_uri(blob, request):
    """ Return download url for the blob

    Args:
        blob:
        request:

    Returns:

    """
    # get URI to download blob
    blob_download_uri = request.build_absolute_uri(reverse("core_main_app_rest_blob_download"))
    # get download handle to blob
    blob_handle = "{0}?id={1}".format(blob_download_uri, str(blob.id))

    return blob_handle
