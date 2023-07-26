""" Url router for the administration site
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from core_main_app.commons.enums import WEB_PAGE_TYPES
from core_main_app.components.blob.admin_site import CustomBlobAdmin
from core_main_app.components.blob.models import Blob
from core_main_app.components.data.admin_site import CustomDataAdmin
from core_main_app.components.data.models import Data
from core_main_app.components.lock.admin_site import CustomDatabaseLockAdmin
from core_main_app.components.lock.models import DatabaseLockObject
from core_main_app.components.template.admin_site import CustomTemplateAdmin
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.admin_site import (
    CustomTemplateVersionManagerAdmin,
)
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.components.template_xsl_rendering.admin_site import (
    CustomTemplateXslRenderingAdmin,
)
from core_main_app.components.template_xsl_rendering.models import (
    TemplateXslRendering,
)
from core_main_app.components.user_preferences.admin_site import (
    CustomUserPreferencesAdmin,
)
from core_main_app.components.user_preferences.models import UserPreferences
from core_main_app.components.web_page_login import api as login_page_api
from core_main_app.components.workspace.admin_site import CustomWorkspaceAdmin
from core_main_app.components.workspace.models import Workspace
from core_main_app.components.xsl_transformation.admin_site import (
    CustomXslTransformationAdmin,
)
from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)
from core_main_app.utils.rendering import admin_render
from core_main_app.views.admin import views as admin_views, ajax as admin_ajax
from core_main_app.views.admin.views import WebPageView
from core_main_app.views.common import views as common_views

admin_urls = [
    re_path(
        r"^login/message/$",
        staff_member_required(
            WebPageView.as_view(
                api=login_page_api,
                get_redirect="core_main_app/admin/web_page/login_page.html",
                post_redirect="core-admin:core_main_app_login_page",
                web_page_type=WEB_PAGE_TYPES["login"],
            )
        ),
        name="core_main_app_login_page",
    ),
    re_path(
        r"^login",
        RedirectView.as_view(url=reverse_lazy("core_main_app_login")),
    ),
    re_path(
        r"^logout",
        RedirectView.as_view(url=reverse_lazy("core_main_app_logout")),
    ),
    re_path(
        r"^data$",
        staff_member_required(
            common_views.ViewData.as_view(
                administration=True,
                template="core_main_app/admin/data/detail.html",
            )
        ),
        name="core_main_app_data_detail",
    ),
    re_path(
        r"^templates$",
        admin_views.manage_templates,
        name="core_main_app_templates",
    ),
    re_path(
        r"^template/upload$",
        admin_views.upload_template,
        name="core_main_app_upload_template",
    ),
    re_path(
        r"^template/data-migration",
        admin_views.data_migration,
        name="core_main_app_data_migration",
    ),
    re_path(
        r"^template/upload/(?P<version_manager_id>\w+)",
        admin_views.upload_template_version,
        name="core_main_app_upload_template_version",
    ),
    re_path(
        r"^template/versions/(?P<version_manager_id>\w+)",
        admin_views.manage_template_versions,
        name="core_main_app_manage_template_versions",
    ),
    re_path(
        r"^template/xslt/(?P<template_id>\w+)",
        staff_member_required(
            common_views.TemplateXSLRenderingView.as_view(
                rendering=admin_render,
                template_name="core_main_app/admin/templates_xslt/main.html",
                save_redirect="core-admin:core_main_app_manage_template_versions",
                back_to_url="core-admin:core_main_app_manage_template_versions",
            )
        ),
        name="core_main_app_template_xslt",
    ),
    re_path(
        r"^dashboard$", admin_views.admin_home, name="core_main_app_admin_home"
    ),
    re_path(
        r"^template/resolve-dependencies",
        admin_ajax.resolve_dependencies,
        name="core_main_app_resolve_dependencies",
    ),
    re_path(
        r"^xslt/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditXSLTView.as_view()),
        name="core_main_app_edit_xslt",
    ),
    re_path(
        r"^xslt$",
        staff_member_required(admin_views.XSLTView.as_view()),
        name="core_main_app_xslt",
    ),
    re_path(
        r"^xslt/upload$",
        staff_member_required(admin_views.UploadXSLTView.as_view()),
        name="core_main_app_upload_xslt",
    ),
    re_path(
        r"^xslt/(?P<pk>[\w-]+)/delete/$",
        staff_member_required(admin_ajax.DeleteXSLTView.as_view()),
        name="core_main_app_delete_xslt",
    ),
    re_path(
        r"^edit-rights/(?P<workspace_id>\w+)$",
        staff_member_required(
            common_views.EditWorkspaceRights.as_view(
                administration=True,
                template="core_main_app/admin/workspaces/edit_rights.html",
            )
        ),
        name="core_main_edit_rights_workspace",
    ),
]


admin.site.register(Data, CustomDataAdmin)
admin.site.register(Blob, CustomBlobAdmin)
admin.site.register(Workspace, CustomWorkspaceAdmin)
admin.site.register(TemplateVersionManager, CustomTemplateVersionManagerAdmin)
admin.site.register(Template, CustomTemplateAdmin)
admin.site.register(XslTransformation, CustomXslTransformationAdmin)
admin.site.register(TemplateXslRendering, CustomTemplateXslRenderingAdmin)
admin.site.register(DatabaseLockObject, CustomDatabaseLockAdmin)
admin.site.register(UserPreferences, CustomUserPreferencesAdmin)


class CoreAdminSite(AdminSite):
    """Admin site for Core apps"""

    def get_urls(self):
        return admin_urls


core_admin_site = CoreAdminSite(name="core-admin")
