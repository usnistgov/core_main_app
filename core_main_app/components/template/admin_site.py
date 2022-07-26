""" Custom admin site for the Template model
"""
from django.contrib import admin


class CustomTemplateAdmin(admin.ModelAdmin):
    """CustomTemplateAdmin"""

    readonly_fields = ["checksum", "hash", "file"]
    exclude = ["_cls"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Templates"""
        return False
