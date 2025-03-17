""" Django REST Framework authentication classes
"""

from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """Token authentication with Bearer keyword
    From: https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
    """

    keyword = "Bearer"
