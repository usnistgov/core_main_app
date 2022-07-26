""" Custom admin site for the Database Lock model
"""
from django.contrib import admin


class CustomDatabaseLockAdmin(admin.ModelAdmin):
    """CustomDatabaseLockAdmin"""

    readonly_fields = ["object"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Locks"""
        return False
