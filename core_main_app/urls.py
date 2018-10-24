""" Url router for the main application
"""
from django.conf.urls import url, include

from core_main_app.views.user import views as user_views, ajax as user_ajax
from core_main_app.views.common import ajax as common_ajax, views as common_views
from core_main_app.utils.rendering import render

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title="REST API")

urlpatterns = [
    url(r'^$', user_views.homepage, name='core_main_app_homepage'),

    url(r'^login', user_views.custom_login, name='core_main_app_login'),
    url(r'^logout', user_views.custom_logout, name='core_main_app_logout'),

    url(r'^rest/', include('core_main_app.rest.urls')),
    url(r'^data',  common_views.ViewData.as_view(), name='core_main_app_data_detail'),
    url(r'^template/versions/(?P<version_manager_id>\w+)', user_views.manage_template_versions,
        name='core_main_app_manage_template_versions'),
    url(r'^template/(?P<pk>[\w-]+)/edit/$', common_ajax.EditTemplateVersionManagerView.as_view(),
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

    url(r'^edit-rights/(?P<workspace_id>\w+)$', common_views.EditWorkspaceRights.as_view(),
        name='core_main_edit_rights_workspace'),

    url(r'^create-workspace', user_ajax.create_workspace, name='core_main_create_workspace'),
    url(r'^change-workspace', user_ajax.LoadFormChangeWorkspace.as_view(), name='core_main_change_workspace'),
    url(r'^assign-workspace', user_ajax.assign_workspace, name='core_main_assign_workspace'),
    url(r'^public-workspace', user_ajax.set_public_workspace, name='core_main_public_workspace'),
    url(r'^private-workspace', user_ajax.set_private_workspace, name='core_main_private_workspace'),

    url(r'^add-user-form', user_ajax.load_add_user_form, name='core_main_edit_rights_users_form'),
    url(r'^add-user-right-to-workspace', user_ajax.add_user_right_to_workspace,
        name='core_main_add_user_right_to_workspace'),
    url(r'^switch-right', user_ajax.switch_right, name='core_main_switch_right'),
    url(r'^remove-rights', user_ajax.remove_user_or_group_rights, name='core_main_remove_rights'),
    url(r'^add-group-form', user_ajax.load_add_group_form, name='core_main_edit_rights_groups_form'),
    url(r'^add-group-right-to-workspace', user_ajax.add_group_right_to_workspace,
        name='core_main_add_group_right_to_workspace'),
    url(r'^docs/api$', schema_view, name='swagger_view'),
    url(r'^tz_detect/', include('tz_detect.urls')),
]
