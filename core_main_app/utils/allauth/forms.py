""" Custom allauth forms
"""

from django.conf import settings


def get_core_signup_form_base_class():
    if (
        "allauth" in settings.INSTALLED_APPS
        and "core_website_app" in settings.INSTALLED_APPS
    ):
        from core_website_app.views.user.forms import RequestAccountForm

        return RequestAccountForm
    # Set to None to raise an error
    return None


class CoreSignupForm(get_core_signup_form_base_class()):
    """Signup Form for Core application"""

    def signup(self, request, user):
        """Implement custom signup method

        Args:
            request:
            user:

        Returns:

        """
        pass
