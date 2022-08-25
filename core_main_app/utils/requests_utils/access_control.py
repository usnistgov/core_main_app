""" Access control utils for HTTP Requests objects
"""
from django.http import HttpRequest
from rest_framework.request import Request

from core_main_app.commons.exceptions import CoreError


def get_request_from_args(*args, **kwargs):
    """get_request_from_args

    Args:

    Returns:
    """
    # get request from parameters
    request = kwargs["request"]
    if (
        isinstance(request, HttpRequest)
        or isinstance(request, Request)
        or request is None
    ):
        return request

    raise CoreError("request parameter improperly set")
