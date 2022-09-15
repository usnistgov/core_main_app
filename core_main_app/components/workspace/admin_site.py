""" Custom admin site for the Workspace model
"""
from django.contrib import admin


class CustomWorkspaceAdmin(admin.ModelAdmin):
    """CustomWorkspaceAdmin"""

    readonly_fields = ["title"]
    exclude = ["read_perm_id", "write_perm_id"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Workspaces"""
        return False
