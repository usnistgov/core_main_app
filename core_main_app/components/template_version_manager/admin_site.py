""" Custom admin site for the Template Version Manager model
"""
from django.contrib import admin


class CustomTemplateVersionManagerAdmin(admin.ModelAdmin):
    """CustomTemplateVersionManagerAdmin"""

    exclude = ["_cls"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Template version managers"""
        return False
