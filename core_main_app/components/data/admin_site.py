""" Custom admin site for the Data model
"""
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.helpers import ActionForm
from django.forms import ChoiceField

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.user import api as user_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.settings import MONGODB_INDEXING


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
            if MONGODB_INDEXING:
                from core_main_app.components.mongo.models import MongoData

                MongoData.update_user_id_from_queryset(queryset, user_id)
            # Display success message
            model_admin.message_user(
                request,
                f"Successfully updated owner of {queryset.count()} Data",
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
                    request, "No workspace found with this id.", messages.WARNING
                )
            # Update workspace
            queryset.update(workspace=workspace)
            if MONGODB_INDEXING:
                from core_main_app.components.mongo.models import MongoData

                workspace_id = workspace.id if workspace else None
                MongoData.update_workspace_id_from_queryset(queryset, workspace_id)
            # Display success message
            model_admin.message_user(
                request,
                f"Successfully updated workspace of {queryset.count()} Data",
                messages.SUCCESS,
            )
    except DoesNotExist as ex:
        model_admin.message_user(request, str(ex), messages.ERROR)
    except Exception as ex:
        model_admin.message_user(request, str(ex), messages.ERROR)


class CustomDataAdmin(admin.ModelAdmin):
    """Custom Data Admin"""

    search_fields = ["title", "vector_column"]
    list_filter = ["template", "user_id", "workspace"]
    list_display = ["title", "last_modification_date", "owner_name", "workspace"]
    action_form = UpdateActionForm
    actions = [update_data_list]
    readonly_fields = ["checksum", "xml_file"]
    exclude = ["vector_column", "dict_content"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding data"""
        return False
