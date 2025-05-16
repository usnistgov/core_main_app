""" Custom admin site for the XslTransformation model
"""

from django.contrib import admin
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.urls import path, reverse

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.xsl_transformation import api as xslt_api
from core_main_app.utils.databases.filefield import (
    diff_files,
    delete_previous_file,
)
from core_main_app.utils.databases.filefield import (
    file_history_display as utils_file_history_display,
)


class CustomXslTransformationAdmin(admin.ModelAdmin):
    """CustomXslTransformationAdmin"""

    exclude = ["file", "file_history"]

    readonly_fields = [
        "checksum",
        "file_history_display",
    ]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding XslTransformation"""
        return False

    @admin.display(description="File History")
    def file_history_display(self, obj):
        """File history display

        Args:
            obj:

        Returns:

        """
        return utils_file_history_display(
            obj,
            diff_url="admin:diff_file_xslt",
            delete_url="admin:delete_file_xslt",
        )

    def get_urls(self):
        """Get custom urls

        Returns:

        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "diff/<int:object_id>/<int:index>/",
                self.admin_site.admin_view(self.diff_file_view),
                name="diff_file_xslt",
            ),
            path(
                "delete_previous_file/<int:object_id>/<int:index>/",
                self.admin_site.admin_view(self.delete_file_view),
                name="delete_file_xslt",
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

        # Get XSLT
        try:
            xslt = xslt_api.get_by_id(object_id)
        except AccessControlError:
            return HttpResponseForbidden("<h1>403 Forbidden</h1>")
        except DoesNotExist:
            return HttpResponseBadRequest("<h1>XSLT not found</h1>")

        # Get diff
        diff = diff_files(
            xslt,
            index,
            model="xsl_transformation",
            content_field="content",
            file_format="XML",
        )
        return render(
            request,
            "core_main_app/admin/diff.html",
            {
                "diff": diff,
                "title": xslt.name,
                "back_url": reverse(
                    "admin:core_main_app_xsltransformation_change",
                    args=[xslt.id],
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

        # Get XSLT
        try:
            xslt = xslt_api.get_by_id(object_id)
        except AccessControlError:
            return HttpResponseForbidden("<h1>403 Forbidden</h1>")
        except DoesNotExist:
            return HttpResponseBadRequest("<h1>XSLT not found</h1>")

        # Delete XSLT
        delete_previous_file(xslt, index, model="xsl_transformation")
        return HttpResponseRedirect(
            reverse(
                "admin:core_main_app_xsltransformation_change",
                args=[object_id],
            )
        )
