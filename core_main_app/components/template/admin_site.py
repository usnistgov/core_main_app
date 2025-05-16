""" Custom admin site for the Template model
"""

from django.contrib import admin
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.urls import reverse, path
from django.utils.safestring import mark_safe

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.template import api as template_api
from core_main_app.utils.databases.filefield import (
    diff_files,
    delete_previous_file,
)
from core_main_app.utils.databases.filefield import (
    file_history_display as utils_file_history_display,
)


class CustomTemplateAdmin(admin.ModelAdmin):
    """CustomTemplateAdmin"""

    readonly_fields = [
        "checksum",
        "hash",
        "file_display",
        "file_history_display",
    ]
    exclude = ["_cls", "file", "file_history"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Templates"""
        return False

    @admin.display(description="File")
    def file_display(self, obj):
        """Display file field

        Args:
            obj:

        Returns:

        """
        if obj.file:
            template_url = reverse(
                "core_main_app_rest_template_download", args=[obj.id]
            )
            return mark_safe(f"<a href={template_url}>{obj.file}</a>")
        return "No file"

    @admin.display(description="File History")
    def file_history_display(self, obj):
        """File History

        Args:
            obj:

        Returns:

        """
        return utils_file_history_display(
            obj,
            diff_url="admin:diff_file_template",
            delete_url="admin:delete_file_template",
        )

    def get_urls(self):
        """Get custom admin urls

        Returns:

        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "diff/<int:object_id>/<int:index>/",
                self.admin_site.admin_view(self.diff_file_view),
                name="diff_file_template",
            ),
            path(
                "delete_previous_file/<int:object_id>/<int:index>/",
                self.admin_site.admin_view(self.delete_file_view),
                name="delete_file_template",
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

        # Get template
        try:
            template = template_api.get_by_id(object_id, request=request)
        except AccessControlError:
            return HttpResponseForbidden("<h1>403 Forbidden</h1>")
        except DoesNotExist:
            return HttpResponseBadRequest("<h1>Template not found</h1>")

        # Get diff
        diff = diff_files(
            template,
            index,
            model="template",
            content_field="content",
            file_format=template.format,
        )
        return render(
            request,
            "core_main_app/admin/diff.html",
            {
                "diff": diff,
                "title": template.filename,
                "back_url": reverse(
                    "admin:core_main_app_template_change", args=[template.id]
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

        # Get template
        try:
            template = template_api.get_by_id(object_id, request=request)
        except AccessControlError:
            return HttpResponseForbidden("<h1>403 Forbidden</h1>")
        except DoesNotExist:
            return HttpResponseBadRequest("<h1>Template not found</h1>")

        # Delete template
        delete_previous_file(template, index, model="template")
        return HttpResponseRedirect(
            reverse("admin:core_main_app_template_change", args=[object_id])
        )
