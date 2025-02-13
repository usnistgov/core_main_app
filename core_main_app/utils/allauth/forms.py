""" Custom allauth forms
"""

from allauth.account.forms import SignupForm as ASignupForm
from allauth.socialaccount.forms import SignupForm as SASignupForm
from captcha.fields import CaptchaField


class CoreAccountSignupForm(ASignupForm):
    """Signup Form for Core application"""

    captcha = CaptchaField()

    field_order = ["email", "username", "password1", "password2", "captcha"]

    def signup(self, request, user):
        """Implement custom signup method

        Args:
            request:
            user:

        Returns:

        """
        pass


class CoreSocialAccountSignupForm(SASignupForm):
    """Signup Form for Core application"""

    captcha = CaptchaField()

    field_order = ["email", "username", "captcha"]
