""" Custom admin site for the XslTransformation model
"""
from django.contrib import admin


class CustomXslTransformationAdmin(admin.ModelAdmin):
    """CustomXslTransformationAdmin"""

    readonly_fields = ["checksum", "file"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding XslTransformation"""
        return False
