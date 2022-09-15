""" Core main app user views
"""
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.staticfiles import finders
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED

from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.components.web_page_login import api as web_page_login_api
from core_main_app.settings import INSTALLED_APPS, PASSWORD_RESET_DOMAIN_OVERRIDE
from core_main_app.utils.markdown_parser import parse
from core_main_app.utils.rendering import render
from core_main_app.views.user.forms import LoginForm

if "defender" in INSTALLED_APPS:
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
    if "defender" in INSTALLED_APPS:
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

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        next_page = request.POST["next_page"]

        try:
            user = authenticate(username=username, password=password)

            if not user.is_active:
                return render(
                    request,
                    "core_main_app/user/login/main.html",
                    context={
                        "login_form": LoginForm(initial={"next_page": next_page}),
                        "login_locked": True,
                        "with_website_features": "core_website_app" in INSTALLED_APPS,
                    },
                )

            login(request, user)

            return _login_redirect(next_page)
        except Exception:
            return render(
                request,
                "core_main_app/user/login/main.html",
                context={
                    "login_form": LoginForm(initial={"next_page": next_page}),
                    "login_error": True,
                    "with_website_features": "core_website_app" in INSTALLED_APPS,
                },
            )
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse("core_main_app_homepage"))

        next_page = None
        if "next" in request.GET:
            next_page = request.GET["next"]

        # build the context
        context = {
            "login_form": LoginForm(initial={"next_page": next_page}),
            "with_website_features": "core_website_app" in INSTALLED_APPS,
        }
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
    logout(request)
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
        assets["js"] = [{"path": "core_main_app/js/homepage.js", "is_raw": False}]

    return render(request, "core_main_app/user/homepage.html", assets=assets)


@login_required(login_url=reverse_lazy("core_main_app_login"))
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

        if not request.user.is_staff and version_manager.user != str(request.user.id):
            raise Exception("You do not have the rights to perform this action.")

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
            context={"error": str(e)},
        )


def get_context_manage_template_versions(version_manager, object_name="Template"):
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


def custom_reset_password(
    request,
    template_name="core_main_app/user/registration/password_reset_form.html",
    email_template_name="core_main_app/user/registration/password_reset_email.html",
    subject_template_name="core_main_app/user/registration/password_reset_subject.txt",
    password_reset_form=PasswordResetForm,
    token_generator=default_token_generator,
    post_reset_redirect=None,
    from_email=None,
    extra_context=None,
    html_email_template_name=None,
    extra_email_context=None,
):
    """Custom reset password page.

    Parameters:
    :param request:
    :param template_name:
    :param email_template_name:
    :param subject_template_name:
    :param password_reset_form:
    :param token_generator:
    :param post_reset_redirect:
    :param from_email:
    :param extra_context:
    :param extra_email_context:
    :param html_email_template_name:

    Returns:
    :return request
    """

    if post_reset_redirect is None:
        post_reset_redirect = reverse("password_reset_done")
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                "use_https": request.is_secure(),
                "token_generator": token_generator,
                "from_email": from_email,
                "email_template_name": email_template_name,
                "subject_template_name": subject_template_name,
                "request": request,
                "html_email_template_name": html_email_template_name,
                "extra_email_context": extra_email_context,
                "domain_override": PASSWORD_RESET_DOMAIN_OVERRIDE,
            }
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        "form": form,
        "title": "Password reset",
    }
    if extra_context is not None:
        context.update(extra_context)

    return render(request, template_name, context=context)


def custom_password_reset_done(
    request,
    template_name="core_main_app/user/registration/password_reset_done.html",
    extra_context=None,
):
    """Custom password reset done page.

    Parameters:
    :param request:
    :param template_name:
    :param extra_context:

    Returns:
    :return request
    """

    context = {
        "title": "Password reset sent",
    }

    assets = {"css": ["core_main_app/user/css/registration.css"]}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template_name, assets=assets, context=context)


def custom_password_reset_confirm(
    request,
    uidb64=None,
    token=None,
    template_name="core_main_app/user/registration/password_reset_confirm.html",
    token_generator=default_token_generator,
    set_password_form=SetPasswordForm,
    post_reset_redirect=None,
    extra_context=None,
):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.

        Parameters:
        :param request:
        :param uidb64:
        :param token:
        :param template_name:
        :param token_generator:
        :param set_password_form:
        :param post_reset_redirect:
        :param extra_context:

        Returns:
        :return request
    """

    user_model = get_user_model()

    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse("password_reset_complete")
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = user_model._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = "Enter new password"
        if request.method == "POST":
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = "Password reset unsuccessful"
    context = {
        "form": form,
        "title": title,
        "validlink": validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    return render(request, template_name, context=context)


def custom_password_reset_complete(
    request,
    template_name="core_main_app/user/registration/password_reset_complete.html",
    extra_context=None,
):
    """
    Custom password reset complete page.

        Parameters:
        :param request:
        :param template_name:
        :param extra_context:

        Returns:
        :return request
    """
    context = {
        "login_url": resolve_url(settings.LOGIN_URL),
        "title": "Password reset complete",
    }

    assets = {"css": ["core_main_app/user/css/registration.css"]}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template_name, context=context, assets=assets)


def saml2_failure(request, exception=None, status=403, **kwargs):
    """Renders a simple template with an error message."""

    return render(
        request,
        "core_main_app/user/login/saml2_error.html",
        context={
            "with_website_features": "core_website_app" in INSTALLED_APPS,
        },
    )
