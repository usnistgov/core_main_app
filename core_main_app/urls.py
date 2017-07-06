""" Url router for the main application
"""
from django.conf.urls import url, include

import core_main_app.views.user.views as user_views
from core_main_app.utils.rendering import render
from views.common import ajax as common_ajax, views as common_views

urlpatterns = [
    url(r'^$', user_views.homepage, name='core_main_app_homepage'),

    url(r'^login', user_views.custom_login, name='core_main_app_login'),
    url(r'^logout', user_views.custom_logout, name='core_main_app_logout'),

    url(r'^rest/', include('core_main_app.rest.urls')),
    url(r'^data', user_views.data_detail, name='core_main_app_data_detail'),

    url(r'^template/versions/(?P<version_manager_id>\w+)', user_views.manage_template_versions,
        name='core_main_app_manage_template_versions'),
    url(r'^template/edit', common_ajax.edit_template_version_manager,
        name='core_main_app_edit_template'),
    url(r'^template/disable', common_ajax.disable_version_manager,
        name='core_main_app_disable_template'),
    url(r'^template/restore', common_ajax.restore_version_manager,
        name='core_main_app_restore_template'),

    url(r'^template/version/disable', common_ajax.disable_template_version_from_version_manager,
        name='core_main_app_disable_template_version'),
    url(r'^template/version/restore', common_ajax.restore_template_version_from_version_manager,
        name='core_main_app_restore_template_version'),
    url(r'^template/version/current', common_ajax.set_current_template_version_from_version_manager,
        name='core_main_app_set_current_template_version'),

    url(r'^xslt$', common_views.XSLTView.as_view(), name='core_main_app_xslt'),
    url(r'^xslt/upload$', common_views.UploadXSLTView.as_view(), name='core_main_app_upload_xslt'),
    url(r'^template/xslt/(?P<template_id>\w+)',
        common_views.TemplateXSLRenderingView.as_view(
            rendering=render,
            template_name="core_main_app/common/templates_xslt/main.html",
            save_redirect="core_main_app_manage_template_versions"
        ),
        name='core_main_app_template_xslt'),
]
