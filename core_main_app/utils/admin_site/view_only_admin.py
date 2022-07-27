""" View Only Admin
"""
from django.contrib import admin


class ViewOnlyAdmin(admin.ModelAdmin):
    """ViewOnlyAdmin"""

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding objects"""
        return False

    def has_change_permission(self, request, obj=None):
        """Prevent from manually updating objects"""
        return False
