""" Form needed for the user part of everything
"""
from django import forms

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.user import api as user_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.labels import get_data_label


class LoginForm(forms.Form):
    """Custom login form for the user"""

    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(
        label="Password", required=True, widget=forms.PasswordInput
    )

    next_page = forms.CharField(widget=forms.HiddenInput)


class GroupRightForm(forms.Form):
    """
    Form to select group to add rights.
    """

    groups = forms.MultipleChoiceField(
        label="", required=True, widget=forms.SelectMultiple()
    )
    GROUPS_OPTIONS = []

    def __init__(self, groups_with_no_access):
        self.GROUPS_OPTIONS = []

        # We sort by name, case sensitive
        sort_groups = sorted(groups_with_no_access, key=lambda s: s.name.lower())

        # We add them
        for group in sort_groups:
            self.GROUPS_OPTIONS.append((group.id, group.name))

        super().__init__()
        self.fields["groups"].choices = []
        self.fields["groups"].choices = self.GROUPS_OPTIONS


class UserRightForm(forms.Form):
    """
    Form to select user to add rights.
    """

    users = forms.MultipleChoiceField(
        label="", required=True, widget=forms.SelectMultiple()
    )
    USERS_OPTIONS = []

    def __init__(self, users_with_no_access):
        self.USERS_OPTIONS = []

        # We sort by username, case sensitive
        sort_users = sorted(users_with_no_access, key=lambda s: s.username.lower())

        # We add them
        for user in sort_users:
            self.USERS_OPTIONS.append((user.id, user.username))

        super().__init__()
        self.fields["users"].choices = []
        self.fields["users"].choices = self.USERS_OPTIONS


class WorkspaceForm(forms.Form):
    """
    Form to create the workspace.
    """

    workspace_name = forms.CharField(max_length=100)


class ChangeWorkspaceForm(forms.Form):
    """
    Form to select a workspace.
    """

    workspaces = forms.ChoiceField(
        label="", required=True, widget=forms.Select(attrs={"class": "form-control"})
    )
    WORKSPACES_OPTIONS = []

    def __init__(
        self,
        user,
        list_current_workspace=None,
        is_administration=False,
        show_global_workspace=False,
    ):
        self.WORKSPACES_OPTIONS = []
        self.WORKSPACES_OPTIONS.append(("", "-----------"))

        if not list_current_workspace:
            list_current_workspace = []
        # We retrieve all workspaces with write access, or all workspaces if administration
        if is_administration:
            all_workspaces = workspace_api.get_all()
        else:
            all_workspaces = list(
                workspace_api.get_all_workspaces_with_write_access_by_user(user)
            )
            if show_global_workspace:
                workspace_global = workspace_api.get_global_workspace()
                if workspace_global not in all_workspaces:
                    all_workspaces.append(workspace_global)

        if len(all_workspaces) == 0:
            raise DoesNotExist(
                "You don't have access to any workspaces with sufficient rights to assign a "
                + get_data_label()
                + "."
            )

        # We sort by title, case insensitive
        sort_workspaces = sorted(all_workspaces, key=lambda s: s.title.lower())

        # We add them
        for workspace in sort_workspaces:
            is_workspace_global = workspace_api.is_workspace_global(workspace)
            if (
                list_current_workspace == []
                or (
                    len(list_current_workspace) > 0
                    and workspace not in list_current_workspace
                )
            ) and (
                (show_global_workspace and is_workspace_global)
                or not is_workspace_global
            ):

                self.WORKSPACES_OPTIONS.append(
                    (
                        workspace.id,
                        workspace.title
                        + " ("
                        + (
                            "GLOBAL"
                            if is_workspace_global
                            else user_api.get_user_by_id(workspace.owner).username
                        )
                        + ")",
                    )
                )

        super().__init__()
        self.fields["workspaces"].choices = []
        self.fields["workspaces"].choices = self.WORKSPACES_OPTIONS
