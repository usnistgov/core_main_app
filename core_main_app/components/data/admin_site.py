""" Custom admin site for the Data model
"""

from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.helpers import ActionForm
from django.forms import ChoiceField
from django.http import (
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.data import api as data_api
from core_main_app.components.user import api as user_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.admin_site.model_admin_class import (
    get_base_model_admin_class,
)
from core_main_app.utils.databases.filefield import (
    diff_files,
    delete_previous_file,
)
from core_main_app.utils.databases.filefield import (
    file_history_display as utils_file_history_display,
)
from core_main_app.utils.labels import get_data_label


class UpdateActionForm(ActionForm):
    """Action form for data update"""

    user_id = ChoiceField(label="Owner:", required=False)
    workspace = ChoiceField(label="Workspace:", required=False)

    WORKSPACES_OPTIONS = []
    USER_OPTIONS = []

    def __init__(self, *args, **kwargs):
        # Clear workspace choices
        self.WORKSPACES_OPTIONS = list()
        # Add empty option (no workspace change)
        self.WORKSPACES_OPTIONS.append(("", ""))
        # Add None option (remove from workspace)
        self.WORKSPACES_OPTIONS.append(("None", "Remove from Workspace"))
        # Get all workspaces
        all_workspaces = workspace_api.get_all()
        # Add all workspaces options
        for workspace in all_workspaces:
            self.WORKSPACES_OPTIONS.append((workspace.id, workspace.title))

        # Clear user choices
        self.USERS_OPTIONS = list()
        # Add empty option (no user change)
        self.USERS_OPTIONS.append(("", ""))
        # Get all active users
        all_users = sorted(
            user_api.get_active_users(), key=lambda s: s.username.lower()
        )

        # Add all users options
        for user in all_users:
            self.USERS_OPTIONS.append((user.id, user.username))

        # Init action form
        super().__init__(*args, **kwargs)
        # Set choices
        self.fields["user_id"].choices = list()
        self.fields["user_id"].choices = self.USERS_OPTIONS
        self.fields["workspace"].choices = list()
        self.fields["workspace"].choices = self.WORKSPACES_OPTIONS


def update_data_list(model_admin, request, queryset):
    """Update data list

    Args:
        model_admin:
        request:
        queryset:

    Returns:

    """
    try:
        # Check if user_id parameter provided
        if "user_id" in request.POST and request.POST["user_id"] != "":
            # Get user id
            user_id = (
                None
                if request.POST["user_id"] == "None"
                else str(request.POST["user_id"])
            )
            # Check if user exists
            try:
                user_api.get_user_by_id(user_id)
            except DoesNotExist:
                model_admin.message_user(
                    request, "No user found with this id.", messages.WARNING
                )
            # Update user
            queryset.update(user_id=user_id)
            # No signals on queryset, start update in mongo
            if settings.MONGODB_INDEXING:
                from core_main_app.components.mongo.models import MongoData

                MongoData.update_user_id_from_queryset(queryset, user_id)
            # Display success message
            model_admin.message_user(
                request,
                f"Owner updated for {queryset.count()} {get_data_label()}.",
                messages.SUCCESS,
            )
        # Check if workspace_id parameter provided
        if "workspace" in request.POST and request.POST["workspace"] != "":
            # Get workspace
            workspace = (
                None
                if request.POST["workspace"] == "None"
                else request.POST["workspace"]
            )
            # Check if workspace exists
            try:
                workspace = (
                    workspace_api.get_by_id(workspace)
                    if workspace is not None
                    else None
                )
            except DoesNotExist:
                model_admin.message_user(
                    request,
                    "No workspace found with this id.",
                    messages.WARNING,
                )
            # Update workspace
            queryset.update(workspace=workspace)
            if settings.MONGODB_INDEXING:
                from core_main_app.components.mongo.models import MongoData

                workspace_id = workspace.id if workspace else None
                MongoData.update_workspace_id_from_queryset(
                    queryset, workspace_id
                )
            # Display success message
            model_admin.message_user(
                request,
                f"Workspace updated for {queryset.count()} {get_data_label()}.",
                messages.SUCCESS,
            )
    except DoesNotExist as ex:
        model_admin.message_user(request, str(ex), messages.ERROR)
    except Exception as ex:
        model_admin.message_user(request, str(ex), messages.ERROR)


class CustomDataAdmin(get_base_model_admin_class("Data")):
    """Custom Data Admin"""

    search_fields = ["title", "vector_column"]
    list_filter = ["template", "user_id", "workspace"]
    list_display = [
        "title",
        "last_modification_date",
        "owner_name",
        "workspace",
    ]
    action_form = UpdateActionForm
    actions = [update_data_list]
    readonly_fields = [
        "checksum",
        "file_display",
        "file_history_display",
    ]
    exclude = ["vector_column", "dict_content", "file", "file_history"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding data"""
        return False

    @admin.display(description="File")
    def file_display(self, obj):
        """Display file field

        Args:
            obj:

        Returns:

        """
        if obj.file:
            data_url = reverse(
                "core_main_app_rest_data_download", args=[obj.id]
            )
            return mark_safe(f"<a href={data_url}>{obj.file}</a>")
        return "No file"

    @admin.display(description="File History")
    def file_history_display(self, obj):
        """File history display

        Args:
            obj:

        Returns:

        """
        return utils_file_history_display(
            obj,
            diff_url="admin:diff_file_data",
            delete_url="admin:delete_file_data",
        )

    def get_urls(self):
        """Get custom urls

        Args:

        Returns:

        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "diff/<int:object_id>/<int:index>/",
                self.admin_site.admin_view(self.diff_file_view),
                name="diff_file_data",
            ),
            path(
                "delete_previous_file/<int:object_id>/<int:index>/",
                self.admin_site.admin_view(self.delete_file_view),
                name="delete_file_data",
            ),
        ]
        return custom_urls + urls

    def diff_file_view(self, request, object_id, index):
        """Diff file view

        Args:
            request:
            object_id:
            index:

        Returns:

        """
        # Check if user is superuser
        if not request.user.is_superuser:
            return HttpResponseForbidden("<h1>403 Forbidden</h1>")

        # Get data
        try:
            data = data_api.get_by_id(object_id, user=request.user)
        except AccessControlError:
            return HttpResponseForbidden("<h1>403 Forbidden</h1>")
        except DoesNotExist:
            return HttpResponseBadRequest("<h1>Data not found</h1>")

        # Get diff
        diff = diff_files(
            data,
            index,
            model="data",
            content_field="content",
            file_format=data.template.format,
        )
        return render(
            request,
            "core_main_app/admin/diff.html",
            {
                "diff": diff,
                "title": data.title,
                "back_url": reverse(
                    "admin:core_main_app_data_change", args=[data.id]
                ),
            },
        )

    def delete_file_view(self, request, object_id, index):
        """Delete file view

        Args:
            request:
            object_id:
            index:

        Returns:

        """
        # Check if user is superuser
        if not request.user.is_superuser:
            return HttpResponseForbidden("<h1>403 Forbidden</h1>")

        # Get data
        try:
            data = data_api.get_by_id(object_id, user=request.user)
        except AccessControlError:
            return HttpResponseForbidden("<h1>403 Forbidden</h1>")
        except DoesNotExist:
            return HttpResponseBadRequest("<h1>Data not found</h1>")

        # Delete file
        delete_previous_file(data, index, model="data")
        return HttpResponseRedirect(
            reverse("admin:core_main_app_data_change", args=[object_id])
        )
