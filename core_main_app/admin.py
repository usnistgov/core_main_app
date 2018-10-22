""" Url router for the administration site
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

import core_main_app.components.web_page_login.api as login_page_api
from core_main_app.commons.enums import WEB_PAGE_TYPES
from core_main_app.utils.rendering import admin_render
from core_main_app.views.admin import views as admin_views, ajax as admin_ajax
from core_main_app.views.admin.views import WebPageView
from core_main_app.views.common import views as common_views

admin_urls = [
    url(r'^login/message/$',
        WebPageView.as_view(api=login_page_api,
                            get_redirect='core_main_app/admin/web_page/login_page.html',
                            post_redirect='admin:core_main_app_login_page',
                            web_page_type=WEB_PAGE_TYPES["login"]),
        name='core_main_app_login_page'),
    url(r'^login', RedirectView.as_view(url=reverse_lazy("core_main_app_login"))),
    url(r'^logout', RedirectView.as_view(url=reverse_lazy("core_main_app_logout"))),
    url(r'^data$', common_views.ViewData.as_view(administration=True,
                                                 template='core_main_app/admin/data/view_data.html'),
        name='core_main_app_data_detail'),
    url(r'^templates$', admin_views.manage_templates, name='core_main_app_templates'),
    url(r'^template/upload$', admin_views.upload_template,
        name='core_main_app_upload_template'),
    url(r'^template/upload/(?P<version_manager_id>\w+)', admin_views.upload_template_version,
        name='core_main_app_upload_template_version'),
    url(r'^template/versions/(?P<version_manager_id>\w+)', admin_views.manage_template_versions,
        name='core_main_app_manage_template_versions'),
    url(r'^template/xslt/(?P<template_id>\w+)',
        common_views.TemplateXSLRenderingView.as_view(
            rendering=admin_render,
            template_name="core_main_app/admin/templates_xslt/main.html",
            save_redirect="admin:core_main_app_manage_template_versions",
            back_to_url="admin:core_main_app_manage_template_versions"
        ),
        name='core_main_app_template_xslt'),
    url(r'^dashboard$', admin_views.admin_home, name='core_main_app_admin_home'),

    url(r'^template/resolve-dependencies', admin_ajax.resolve_dependencies,
        name='core_main_app_resolve_dependencies'),
    url(r'^xslt/(?P<pk>[\w-]+)/edit/$', admin_ajax.EditXSLTView.as_view(),
        name='core_main_app_edit_xslt'),
    url(r'^xslt$', admin_views.XSLTView.as_view(), name='core_main_app_xslt'),
    url(r'^xslt/upload$', admin_views.UploadXSLTView.as_view(), name='core_main_app_upload_xslt'),
    url(r'^xslt/(?P<pk>[\w-]+)/delete/$',
        admin_ajax.DeleteXSLTView.as_view(),
        name='core_main_app_delete_xslt'),
    url(r'^edit-rights/(?P<workspace_id>\w+)$',
        common_views.EditWorkspaceRights.as_view(
            administration=True,
            template="core_main_app/admin/workspaces/edit_rights.html"),
        name='core_main_edit_rights_workspace'),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls

# Admin part for the Site model is not useful in this application
admin.site.unregister(Site)
