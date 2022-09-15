""" Custom admin site for the Blob model
"""
from django.contrib import admin


class CustomBlobAdmin(admin.ModelAdmin):
    """CustomBlobAdmin"""

    readonly_fields = ["checksum", "blob"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Blobs"""
        return False
