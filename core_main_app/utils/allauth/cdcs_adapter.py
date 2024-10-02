""" Allauth account adapter for the CDCS
"""

from allauth.account.adapter import DefaultAccountAdapter
from core_website_app.components.account_request import (
    api as account_request_api,
)


class CDCSAccountAdapter(DefaultAccountAdapter):
    """CDCSAccountAdapter"""

    def save_user(self, request, user, form, commit=True):
        """
        Create an inactive user and an account request
        instead of an active user.
        """
        user = super().save_user(request, user, form, commit=False)
        user.is_active = False
        account_request_api.insert(user)
        return user
