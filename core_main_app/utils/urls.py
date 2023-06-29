""" Urls utils
"""

import re

from django.urls import reverse, re_path, include
from django.conf import settings


def get_template_download_pattern():
    """Return regex pattern to match an url to download a template.

    Returns:

    """
    # build django url to download a template
    download_template_url = reverse(
        "core_main_app_rest_template_download", kwargs={"pk": "template_id"}
    )
    # make url a regex
    download_template_regex = download_template_url.replace(
        "template_id", r"(?P<pk>\w+)"
    )
    # compile regex
    pattern = re.compile(download_template_regex)

    return pattern


def get_blob_download_regex(xml_string):
    """Return regex pattern to match an url to download a blob.

    Returns:

    """
    # build django url to download a blob
    download_blob_url = reverse(
        "core_main_app_rest_blob_download", kwargs={"pk": "blob_id"}
    )
    download_blob_url = download_blob_url.replace("blob_id/", "")
    # make the regex
    regex = ">(http[s]?:[^<>]+" + download_blob_url + "[0-9]+/?)<"
    return re.findall(regex, xml_string)


def get_auth_urls():
    """Get auth urls

    Returns:

    """
    urlpatterns = []

    if settings.ENABLE_SAML2_SSO_AUTH:
        from djangosaml2 import views as saml2_views

        urlpatterns.append(re_path(r"saml2/", include("djangosaml2.urls")))
        urlpatterns.append(
            re_path(
                r"^saml2/login",
                saml2_views.LoginView.as_view(),
                name="core_main_app_login",
            )
        )
        urlpatterns.append(
            re_path(
                r"^saml2/logout",
                saml2_views.LogoutInitView.as_view(),
                name="core_main_app_logout",
            )
        )
    else:
        from core_main_app.views.user import views as user_views
        from django.contrib.auth import views as auth_views

        urlpatterns.append(
            re_path(
                r"^login",
                user_views.custom_login,
                name="core_main_app_login",
            )
        )
        urlpatterns.append(
            re_path(
                r"^logout",
                user_views.custom_logout,
                name="core_main_app_logout",
            )
        )
        urlpatterns.append(
            re_path(
                "password_change/$",
                auth_views.PasswordChangeView.as_view(),
                name="password_change",
            )
        )
        urlpatterns.append(
            re_path(
                "password_change/done/$",
                auth_views.PasswordChangeDoneView.as_view(),
                name="password_change_done",
            )
        )
        urlpatterns.append(
            re_path(
                "password_reset/$",
                auth_views.PasswordResetView.as_view(),
                name="password_reset",
            )
        )
        urlpatterns.append(
            re_path(
                "password_reset/done/$",
                auth_views.PasswordResetDoneView.as_view(),
                name="password_reset_done",
            )
        )
        urlpatterns.append(
            re_path(
                r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
                auth_views.PasswordResetConfirmView.as_view(),
                name="password_reset_confirm",
            )
        )
        urlpatterns.append(
            re_path(
                r"^reset/done/$",
                auth_views.PasswordResetCompleteView.as_view(),
                name="password_reset_complete",
            )
        )
    return urlpatterns
