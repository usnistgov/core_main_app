"""Utils for the python requests package"""

import requests

from core_main_app.settings import SSL_CERTIFICATES_DIR
from core_main_app.utils.validation.url_validation import validate_request_url


def send_get_request(url, params=None, **kwargs):
    """Send a GET request using python requests.

    Args:
        url:
        params:
        **kwargs:

    Returns:

    """
    validate_request_url(url)
    if "verify" not in kwargs:
        kwargs["verify"] = SSL_CERTIFICATES_DIR
    return requests.get(url, params, **kwargs)


def send_post_request(url, data=None, json=None, **kwargs):
    """Send a POST request using python requests.

    Args:
        url:
        data:
        json:
        **kwargs:

    Returns:

    """
    validate_request_url(url)
    if "verify" not in kwargs:
        kwargs["verify"] = SSL_CERTIFICATES_DIR
    return requests.post(url, data, json, **kwargs)


def send_put_request(url, data=None, **kwargs):
    """Send a PUT request using python requests.

    Args:
        url:
        data:
        **kwargs:

    Returns:

    """
    validate_request_url(url)
    if "verify" not in kwargs:
        kwargs["verify"] = SSL_CERTIFICATES_DIR
    return requests.put(url, data, **kwargs)


def send_delete_request(url, **kwargs):
    """Send a DELETE request using python requests.

    Args:
        url:
        **kwargs:

    Returns:

    """
    validate_request_url(url)
    if "verify" not in kwargs:
        kwargs["verify"] = SSL_CERTIFICATES_DIR
    return requests.delete(url, **kwargs)
