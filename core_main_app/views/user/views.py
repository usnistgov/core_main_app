""" Core main app user views
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED
from core_main_app.utils.rendering import render
import core_main_app.components.data.api as data_api
from core_main_app.views.user.forms import LoginForm


def custom_login(request):
    """ Custom login page.
    
        Parameters:
            request: 
    
        Returns:
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = authenticate(username=username, password=password)

            if not user.is_active:
                return render(request, "core_main_app/user/login.html",
                              context={'login_form': LoginForm(), 'login_locked': True})

            login(request, user)

            return redirect(reverse("core_main_app_homepage"))
        except Exception as e:
            return render(request, "core_main_app/user/login.html",
                          context={'login_form': LoginForm(), 'login_error': True})
    elif request.method == "GET":
        if request.user.is_authenticated():
            return redirect(reverse("core_main_app_homepage"))

        return render(request, "core_main_app/user/login.html", context={'login_form': LoginForm()})
    else:
        return HttpResponse(status=HTTP_405_METHOD_NOT_ALLOWED)


def custom_logout(request):
    """ Custom logout page.
    
        Parameters:
            request: 
    
        Returns:
    """
    logout(request)
    return redirect(reverse("core_main_app_login"))


def homepage(request):
    """ Homepage for the website

        Parameters:
            request:

        Returns:
    """
    assets = {
        "js": []
    }

    if finders.find("core_main_app/css/homepage.css") is not None:
        assets["css"] = ["core_main_app/css/homepage.css"]

    if finders.find("core_main_app/js/homepage.js") is not None:
        assets["js"].append(
            {
                "path": "core_main_app/js/homepage.js",
                "is_raw": False
            }
        )

    return render(request, "core_main_app/user/homepage.html", assets=assets)


def data_detail(request):
    """

    Args:
        request:

    Returns:

    """
    data_id = request.GET['id']

    try:
        data = data_api.get_by_id(data_id)
    except:
        # TODO: catch good exception, redirect to error page
        pass

    context = {
        'data': data
    }

    assets = {
        "js": [
            {
                "path": 'core_main_app/common/js/XMLTree.js',
                "is_raw": False
            },
            {
                "path": 'core_main_app/user/js/data/detail.js',
                "is_raw": False
            },
        ],
        "css": ["core_main_app/common/css/XMLTree.css"],
    }

    return render(request, 'core_main_app/user/data/detail.html', context=context, assets=assets)
