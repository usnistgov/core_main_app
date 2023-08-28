""" Core main app user views
"""
from django.conf import settings
from django.contrib import auth as django_auth
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from pytz import common_timezones as pytz_common_timezones
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.components.user_preferences import (
    api as user_preferences_api,
)
from core_main_app.components.user_preferences.models import UserPreferences
from core_main_app.components.web_page_login import api as web_page_login_api
from core_main_app.utils.markdown_parser import parse
from core_main_app.utils.rendering import render
from core_main_app.views.user.forms import LoginForm

if "defender" in settings.INSTALLED_APPS:
    from defender.decorators import watch_login

    @watch_login()
    def defender_custom_login(request):
        """Custom login page with defender controls.

        Args:
            request:

        Returns:

        """
        return default_custom_login(request)


def custom_login(request):
    """Custom login page calls default page or page with defender if installed.

    Args:
        request:

    Returns:

    """
    if "defender" in settings.INSTALLED_APPS:
        return defender_custom_login(request)
    else:
        return default_custom_login(request)


def default_custom_login(request):
    """Default custom login page.

    Parameters:
        request:

    Returns:
    """

    def _login_redirect(to_page):
        if to_page is not None and to_page != "":
            return redirect(to_page)

        return redirect(reverse("core_main_app_homepage"))

    context = {
        "page_title": "Login",
        "with_website_features": "core_website_app" in settings.INSTALLED_APPS,
        "ENABLE_SAML2_SSO_AUTH": settings.ENABLE_SAML2_SSO_AUTH,
    }
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        next_page = request.POST["next_page"]

        try:
            user = django_auth.authenticate(
                username=username, password=password
            )
            if not user.is_active:
                context.update(
                    {
                        "login_form": LoginForm(
                            initial={"next_page": next_page}
                        ),
                        "login_locked": True,
                    }
                )
                return render(
                    request,
                    "core_main_app/user/login/main.html",
                    context=context,
                )

            django_auth.login(request, user)

            return _login_redirect(next_page)
        except Exception:
            context.update(
                {
                    "login_form": LoginForm(initial={"next_page": next_page}),
                    "login_error": True,
                }
            )
            return render(
                request,
                "core_main_app/user/login/main.html",
                context=context,
            )
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse("core_main_app_homepage"))

        next_page = None
        if "next" in request.GET:
            next_page = request.GET["next"]

        # build the context
        context.update(
            {"login_form": LoginForm(initial={"next_page": next_page})}
        )
        assets = {"css": ["core_main_app/user/css/login.css"]}

        # get the web page login if exist
        web_page_login = web_page_login_api.get()

        if web_page_login:
            # update the context
            context["login_message"] = parse(web_page_login.content)

            # if exist we build assets and modals collection
            assets.update(
                {
                    "js": [
                        {
                            "path": "core_main_app/user/js/login/message.js",
                            "is_raw": False,
                        }
                    ]
                }
            )
            modals = ["core_main_app/user/login/modals/login_message.html"]

            # render the page with context, assets and modals
            return render(
                request,
                "core_main_app/user/login/main.html",
                context=context,
                assets=assets,
                modals=modals,
            )

        # render the page with context, assets
        return render(
            request,
            "core_main_app/user/login/main.html",
            context=context,
            assets=assets,
        )
    else:
        return HttpResponse(status=HTTP_405_METHOD_NOT_ALLOWED)


def custom_logout(request):
    """Custom logout page.

    Parameters:
        request:

    Returns:
    """
    django_auth.logout(request)
    return redirect(reverse("core_main_app_homepage"))


def homepage(request):
    """Homepage for the website

    Parameters:
        request:

    Returns:
    """
    assets = dict()

    if finders.find("core_main_app/css/homepage.css") is not None:
        assets["css"] = ["core_main_app/css/homepage.css"]

    if finders.find("core_main_app/js/homepage.js") is not None:
        assets["js"] = [
            {"path": "core_main_app/js/homepage.js", "is_raw": False}
        ]

    return render(request, "core_main_app/user/homepage.html", assets=assets)


@login_required
def manage_template_versions(request, version_manager_id):
    """View that allows template versions management

    Args:
        request:
        version_manager_id:

    Returns:

    """
    try:
        # get the version manager
        version_manager = template_version_manager_api.get_by_id(
            version_manager_id, request=request
        )

        if not request.user.is_staff and version_manager.user != str(
            request.user.id
        ):
            raise Exception(
                "You do not have the rights to perform this action."
            )

        context = get_context_manage_template_versions(version_manager)
        if "core_parser_app" in settings.INSTALLED_APPS:
            context.update({"module_url": "core_parser_app_template_modules"})

        assets = {
            "js": [
                {
                    "path": "core_main_app/common/js/templates/versions/set_current.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/templates/versions/restore.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/templates/versions/modals/disable.js",
                    "is_raw": False,
                },
            ]
        }

        modals = ["core_main_app/admin/templates/versions/modals/disable.html"]

        # Set page title
        context.update({"page_title": "Template Versions"})

        return render(
            request,
            "core_main_app/common/templates/versions.html",
            assets=assets,
            modals=modals,
            context=context,
        )
    except Exception as e:
        return render(
            request,
            "core_main_app/common/commons/error.html",
            context={"error": str(e), "page_title": "Error"},
        )


def get_context_manage_template_versions(
    version_manager, object_name="Template"
):
    """Get the context to manage the template versions.

    Args:
        version_manager:
        object_name:

    Returns:

    """

    # Use categorized version for easier manipulation in template
    versions = version_manager.version_set
    categorized_versions = {"available": [], "disabled": []}
    for index, version in enumerate(versions, 1):
        indexed_version = {
            "index": index,
            "object": str(version.id),
            "creation_date": version.creation_date,
            "format": version.format,
        }

        if str(version.id) not in version_manager.disabled_versions:
            categorized_versions["available"].append(indexed_version)
        else:
            categorized_versions["disabled"].append(indexed_version)

    context = {
        "object_name": object_name,
        "version_manager": version_manager,
        "categorized_versions": categorized_versions,
    }

    return context


def saml2_failure(request, exception=None, status=403, **kwargs):
    """Renders a simple template with an error message."""

    return render(
        request,
        "core_main_app/user/login/saml2_error.html",
        context={
            "with_website_features": "core_website_app"
            in settings.INSTALLED_APPS,
            "page_title": "Error",
        },
    )


@login_required
def set_timezone(request):
    """Set timezone in session

    Args:
        request:

    Returns:

    """
    try:
        if request.method == "POST":
            user_preferences = _get_preferences(request.user)
            if not user_preferences:
                user_preferences = UserPreferences(
                    user_id=str(request.user.id)
                )
            user_preferences.timezone = request.POST["timezone"]
            user_preferences_api.upsert(user_preferences, request.user)
            request.session["django_timezone"] = user_preferences.timezone
            return redirect("/")
        else:
            user_preferences = _get_preferences(request.user)
            user_timezone = (
                user_preferences.timezone
                if user_preferences and user_preferences.timezone
                else timezone.get_current_timezone().key
            )
            return render(
                request,
                "core_main_app/user/timezone.html",
                context={
                    "timezones": pytz_common_timezones,
                    "timezone": user_timezone,
                },
            )
    except AccessControlError:
        error_message = "Access Forbidden"
        status_code = 403
    except Exception as exception:
        error_message = f"An error occurred: {str(exception)}"
        status_code = 400

    return render(
        request,
        "core_main_app/common/commons/error.html",
        context={
            "error": error_message,
            "status_code": status_code,
            "page_title": "Error",
        },
    )


def _get_preferences(user):
    """Get User Preferences

    Args:
        user: User

    Return:
    """
    try:
        return user_preferences_api.get_by_user(user)
    except DoesNotExist:
        return None
