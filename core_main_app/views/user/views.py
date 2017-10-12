""" Core main app user views
"""
import copy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.http.response import HttpResponse
from django.shortcuts import redirect
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED

import core_main_app.components.data.api as data_api
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.group import api as group_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.settings import INSTALLED_APPS
from core_main_app.utils import group as group_utils
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.rendering import render
from core_main_app.views.user.forms import LoginForm

GROUP = "group"
USER = "user"

ACTION_READ = "action_read"
ACTION_WRITE = "action_write"


def custom_login(request):
    """ Custom login page.
    
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
                return render(request, "core_main_app/user/login.html",
                              context={'login_form': LoginForm(initial={'next_page': next_page}), 'login_locked': True,
                                       'with_website_features': "core_website_app" in INSTALLED_APPS})

            login(request, user)

            return _login_redirect(next_page)
        except Exception as e:
            return render(request, "core_main_app/user/login.html",
                          context={'login_form': LoginForm(initial={'next_page': next_page}), 'login_error': True,
                                   'with_website_features': "core_website_app" in INSTALLED_APPS})
    elif request.method == "GET":
        if request.user.is_authenticated():
            return redirect(reverse("core_main_app_homepage"))

        next_page = None
        if "next" in request.GET:
            next_page = request.GET["next"]

        return render(request, "core_main_app/user/login.html",
                      context={'login_form': LoginForm(initial={"next_page": next_page}),
                               'with_website_features': "core_website_app" in INSTALLED_APPS})
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
    error_message = ''

    try:
        data = data_api.get_by_id(data_id, request.user)

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
    except AccessControlError:
        error_message = 'Access forbidden'
    except exceptions.DoesNotExist:
        error_message = 'Data not found'
    except exceptions.ModelError:
        error_message = 'Model error'
    except Exception, e:
        error_message = 'Unexpected error'

    return render(request, 'core_main_app/common/commons/error.html',
                  context={"error": "Unable to access the requested data: {}.".format(error_message)})


@login_required(login_url='/login')
def manage_template_versions(request, version_manager_id):
    """View that allows template versions management

    Args:
        request:
        version_manager_id:

    Returns:

    """

    # get the version manager
    version_manager = None
    try:
        version_manager = version_manager_api.get(version_manager_id)
    except:
        # TODO: catch good exception, redirect to error page
        pass

    if not request.user.is_staff and version_manager.user != str(request.user.id):
        raise Exception("You don't have the rights to perform this action.")

    context = get_context_manage_template_versions(version_manager)

    assets = {
                "js": [
                    {
                        "path": 'core_main_app/common/js/templates/versions/set_current.js',
                        "is_raw": False
                    },
                    {
                        "path": 'core_main_app/common/js/templates/versions/restore.js',
                        "is_raw": False
                    },
                    {
                        "path": 'core_main_app/common/js/templates/versions/modals/disable.js',
                        "is_raw": False
                    },
                    {
                        "path": 'core_main_app/common/js/backtoprevious.js',
                        "is_raw": True
                    }
                ]
            }

    modals = ["core_main_app/admin/templates/versions/modals/disable.html"]

    return render(request,
                  'core_main_app/common/templates/versions.html',
                  assets=assets,
                  modals=modals,
                  context=context)


def get_context_manage_template_versions(version_manager):
    """ Get the context to manage the template versions.

    Args:
        version_manager:

    Returns:

    """

    # Use categorized version for easier manipulation in template
    versions = version_manager.versions
    categorized_versions = {
        "available": [],
        "disabled": []
    }
    for index, version in enumerate(versions, 1):
        indexed_version = {
            "index": index,
            "object": version
        }

        if version not in version_manager.disabled_versions:
            categorized_versions["available"].append(indexed_version)
        else:
            categorized_versions["disabled"].append(indexed_version)
    version_manager.versions = categorized_versions
    context = {
        'object_name': 'Template',
        "version_manager": version_manager
    }

    return context


def edit_rights(request, workspace_id):
    """ Load page to edit the rights.

    Args:   request
            workspace_id
    Returns:
    """

    try:
        workspace = workspace_api.get_by_id(workspace_id)
    except DoesNotExist as e:
        return HttpResponseBadRequest("The workspace does not exist.")
    except:
        return HttpResponseBadRequest("Something wrong happened.")

    if workspace.owner != str(request.user.id):
        return HttpResponseForbidden("Only the workspace owner can edit the rights.")

    try:
        # Users
        users_read_workspace = workspace_api.get_list_user_can_read_workspace(workspace, request.user)
        users_write_workspace = workspace_api.get_list_user_can_write_workspace(workspace, request.user)

        users_access_workspace = list(set(users_read_workspace + users_write_workspace))
        detailed_users = []
        for user in users_access_workspace:
            detailed_users.append({'object_id': user.id,
                                   'object_name': user.username,
                                   'can_read': user in users_read_workspace,
                                   'can_write': user in users_write_workspace,
                                   })
    except:
        detailed_users = []

    try:
        # Groups
        groups_read_workspace = workspace_api.get_list_group_can_read_workspace(workspace, request.user)
        groups_write_workspace = workspace_api.get_list_group_can_write_workspace(workspace, request.user)

        groups_access_workspace = list(set(groups_read_workspace + groups_write_workspace))
        group_utils.remove_list_object_from_list(groups_access_workspace,
                                                 [group_api.get_anonymous_group(), group_api.get_default_group()])
        detailed_groups = []
        for group in groups_access_workspace:
            detailed_groups.append({'object_id': group.id,
                                    'object_name': group.name,
                                    'can_read': group in groups_read_workspace,
                                    'can_write': group in groups_write_workspace,
                                    })
    except:
        detailed_groups = []

    context = {
        'workspace': workspace,
        'user_data': detailed_users,
        'group_data': detailed_groups,
        'template': "core_main_app/user/workspaces/list/edit_rights_table.html",
        'action_read': ACTION_READ,
        'action_write': ACTION_WRITE,
        'user': USER,
        'group': GROUP,
    }

    assets = {
        "css": ['core_main_app/libs/datatables/1.10.13/css/jquery.dataTables.css',
                'core_main_app/libs/fSelect/css/fSelect.css',
                'core_main_app/common/css/switch.css'],

        "js": [{
                    "path": 'core_main_app/libs/datatables/1.10.13/js/jquery.dataTables.js',
                    "is_raw": True
                },
                {
                    "path": "core_main_app/libs/fSelect/js/fSelect.js",
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/common/js/backtoprevious.js',
                    "is_raw": True
                },
                {
                    "path": 'core_main_app/user/js/workspaces/tables.js',
                    "is_raw": True
                },
                {
                    "path": 'core_main_app/user/js/workspaces/add_user.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/user/js/workspaces/list/modals/switch_right.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/user/js/workspaces/list/modals/remove_rights.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/user/js/workspaces/add_group.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/user/js/workspaces/init.js',
                    "is_raw": False
                }]
    }

    modals = ["core_main_app/user/workspaces/list/modals/add_user.html",
              "core_main_app/user/workspaces/list/modals/switch_right.html",
              "core_main_app/user/workspaces/list/modals/remove_rights.html",
              "core_main_app/user/workspaces/list/modals/add_group.html"]

    return render(request, "core_main_app/user/workspaces/edit_rights.html",
                  context=context,
                  assets=assets,
                  modals=modals)
