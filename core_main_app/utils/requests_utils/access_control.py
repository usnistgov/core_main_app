""" Access control utils for HTTP Requests objects
"""
from django.http import HttpRequest
from rest_framework.request import Request

from core_main_app.commons.exceptions import CoreError

SYSTEM_REQUEST = "SYSTEM_REQUEST"


def get_request_from_args(*args, **kwargs):
    # get request from parameters
    request = kwargs["request"]
    if isinstance(request, HttpRequest) or isinstance(request, Request):
        return request
    # check if request is set to SYSTEM
    if request == SYSTEM_REQUEST:
        return request

    raise CoreError("request parameter improperly set")
