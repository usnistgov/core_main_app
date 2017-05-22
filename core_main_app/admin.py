"""
Url router for the administration site
"""
from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from views.admin import views as admin_views, ajax as admin_ajax

admin_urls = [
    url(r'^login', RedirectView.as_view(url=reverse_lazy("core_main_app_login"))),
    url(r'^logout', RedirectView.as_view(url=reverse_lazy("core_main_app_logout"))),

    url(r'^templates$', admin_views.manage_templates, name='core_main_app_templates'),
    url(r'^template/upload$', admin_views.upload_template,
        name='core_main_app_upload_template'),
    url(r'^template/upload/(?P<version_manager_id>\w+)', admin_views.upload_template_version,
        name='core_main_app_upload_template_version'),
    url(r'^template/versions/(?P<version_manager_id>\w+)', admin_views.manage_template_versions,
        name='core_main_app_manage_template_versions'),
    url(r'^template/xslt/(?P<template_id>\w+)', admin_views.TemplateXSLRenderingView.as_view(),
        name='core_main_app_template_xslt'),
    url(r'^dashboard$', admin_views.admin_home, name='core_main_app_admin_home'),


    url(r'^template/disable', admin_ajax.disable_template,
        name='core_main_app_disable_template'),
    url(r'^template/restore', admin_ajax.restore_template,
        name='core_main_app_restore_template'),
    url(r'^template/version/disable', admin_ajax.disable_template_version,
        name='core_main_app_disable_template_version'),
    url(r'^template/version/restore', admin_ajax.restore_template_version,
        name='core_main_app_restore_template_version'),
    url(r'^template/version/current', admin_ajax.set_current_version,
        name='core_main_app_set_current_template_version'),
    url(r'^template/resolve-dependencies', admin_ajax.resolve_dependencies,
        name='core_main_app_resolve_dependencies'),
    url(r'^template/edit', admin_ajax.edit_template,
        name='core_main_app_edit_template'),

    url(r'^xslt$', admin_views.XSLTView.as_view(), name='core_main_app_xslt'),
    url(r'^xslt/upload$', admin_views.UploadXSLTView.as_view(), name='core_main_app_upload_xslt'),
    url(r'^xslt/edit', admin_ajax.edit_xslt_name, name='core_main_app_edit_xslt'),
    url(r'^xslt/delete', admin_ajax.delete_xslt, name='core_main_app_delete_xslt'),

]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
