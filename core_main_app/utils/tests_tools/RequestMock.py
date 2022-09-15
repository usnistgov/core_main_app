""" Mock a Request object.
"""
import json
from unittest.mock import Mock

from django.contrib.sessions.models import Session
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpRequest
from rest_framework import status
from rest_framework.test import APIRequestFactory


class RequestMock:
    """Represent a request.
    Use this class to simulate an HTTP request.
    """

    @staticmethod
    def do_request_get(view, user, data=None, param=None):
        """Execute a GET HTTP request.
        Args:
            view: View method called by the request.
            user: User for the request.
            data: Data.
            param: View method params.

        Returns:
            Response: Request response.

        """
        return RequestMock._do_request("GET", view, user, data, param)

    @staticmethod
    def do_request_post(
        view, user, data=None, param=None, content_type="application/json"
    ):
        """Execute a POST HTTP request.
        Args:
            view: View method called by the request.
            user: User for the request.
            data: Data.
            param: View method params.

        Returns:
            Response: Request response.
        """
        return RequestMock._do_request("POST", view, user, data, param, content_type)

    @staticmethod
    def do_request_put(
        view, user, data=None, param=None, content_type="application/json"
    ):
        """Execute a PUT HTTP request.
        Args:
            view: View method called by the request.
            user: User for the request.
            data: Data.
            param: View method params.
            content_type: Content-Type of the data passed.

        Returns:
            Response: Request response.

        """
        return RequestMock._do_request("PUT", view, user, data, param, content_type)

    @staticmethod
    def do_request_delete(
        view, user, data=None, param=None, content_type="application/json"
    ):
        """Execute a DELETE HTTP request.
        Args:
            view: View method called by the request.
            user: User for the request.
            data: Data.
            param: View method params.
            content_type: Content-Type of the data passed.

        Returns:
            Response: Request response.

        """
        return RequestMock._do_request("DELETE", view, user, data, param, content_type)

    @staticmethod
    def do_request_patch(
        view, user, data=None, param=None, content_type="application/json"
    ):
        """Execute a PATCH HTTP request.
        Args:
            view: View method called by the request.
            user: User for the request.
            data: Data.
            param: View method params.
            content_type: Content-Type of the data passed.

        Returns:
            Response: Request response.

        """
        return RequestMock._do_request("PATCH", view, user, data, param, content_type)

    @staticmethod
    def _do_request(
        http_method, view, user, data=None, param=None, content_type="application/json"
    ):
        """Execute the http_method request.
        Args:
            http_method: HTTP method.
            view: View method called by the request.
            user: User for the request.
            data: Data.
            param: View method params.
            content_type: Content-Type of the data passed.

        Returns:
            Response: Request response.

        """
        # Pre-process data depending on its content-type. GET request don't have
        # a content-type and the processing is bypassed in this case.
        if http_method != "GET":
            if content_type == "application/json":
                data = json.dumps(data)

        url = "/dummy_url"
        factory = APIRequestFactory()
        # Request by http_method.
        if http_method == "GET":
            request = factory.get(url, data=data)
        elif http_method == "POST":
            request = factory.post(url, data=data, content_type=content_type)
        elif http_method == "PUT":
            request = factory.put(url, data=data, content_type=content_type)
        elif http_method == "DELETE":
            request = factory.delete(url, data=data, content_type=content_type)
        elif http_method == "PATCH":
            request = factory.patch(url, data=data, content_type=content_type)
        else:
            return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # Set the user
        request.user = user
        # Set the session
        request.session = Session(session_key="KEY")
        # i18n. Get django validation messages.
        get_wsgi_application()
        # Do not use CSRF checks.
        request._dont_enforce_csrf_checks = True

        if param:
            view_ = view(request, **param)
        else:
            view_ = view(request)

        return view_


def create_mock_request(user=None):
    """Create a Mock HTTP Request

    Args:
        user:

    Returns:

    """
    mock_request = Mock(spec=HttpRequest)
    mock_request.user = user
    mock_request.session = Session(session_key="KEY")
    return mock_request
