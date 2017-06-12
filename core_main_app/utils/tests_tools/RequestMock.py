""" Mock a Request object.
"""
from django.test import RequestFactory
from django.core.wsgi import get_wsgi_application
import json


class RequestMock(object):
    """ Represent a request.
        Use this class to simulate an HTTP request.
    """

    @staticmethod
    def do_request_get(view, user, data=None):
        """Execute a GET HTTP request.
        Args:
            view: View method called by the request.
            user: User for the request.
            data: Data.

        Returns:
            Response: Request response.

        """
        return RequestMock._do_request("GET", view, user, data)

    @staticmethod
    def do_request_post(view, user, data=None):
        """Execute a POST HTTP request.
        Args:
            view: View method called by the request.
            user: User for the request.
            data: Data.

        Returns:
            Response: Request response.
        """
        return RequestMock._do_request("POST", view, user, data)

    @staticmethod
    def do_request_put(view, user, data=None):
        """Execute a PUT HTTP request.
        Args:
            view: View method called by the request.
            user: User for the request.
            data: Data.

        Returns:
            Response: Request response.

        """
        return RequestMock._do_request("PUT", view, user, data)

    @staticmethod
    def _do_request(http_method, view, user, data=None):
        """Execute the http_method request.
        Args:
            http_method: HTTP method.
            view: View method called by the request.
            user: User for the request.
            data: Data.

        Returns:
            Response: Request response.

        """
        url = "/dummy_url"
        factory = RequestFactory()
        # Request by http_method.
        if http_method == "GET":
            request = factory.get(url, data=data)
        elif http_method == "POST":
            request = factory.post(url, data=data)
        elif http_method == "PUT":
            request = factory.put(url, data=json.dumps(data), content_type="application/json")
        # Set the user
        request.user = user
        # i18n. Get django validation messages.
        get_wsgi_application()
        # Do not use CSRF checks.
        request._dont_enforce_csrf_checks = True

        return view(request)
