"""Url router for the REST API
"""
from django.conf.urls import url
from core_main_app.rest.template import views as template_views
from core_main_app.rest.template_version_manager import views as template_version_manager_views
from core_main_app.rest.data import views as data_views
from core_main_app.rest.blob import views as blob_views

urlpatterns = [
    url(r'^template/download', template_views.download,
        name='core_main_app_rest_template_download'),

    url(r'^template/get', template_views.get_by_id,
        name='core_main_app_rest_template_get_by_id'),

    url(r'^template-version-manager/get/all/global$', template_version_manager_views.get_all_globals,
        name='core_main_app_rest_template_version_manager_get_all_globals'),

    url(r'^template-version-manager/get/active/user$', template_version_manager_views.get_active_by_user,
        name='core_main_app_rest_template_version_manager_get_active_by_user'),

    url(r'^template-version-manager/get$', template_version_manager_views.get_by_id,
        name='core_main_app_rest_template_version_manager_get'),

    url(r'^template', template_views.template,
        name='core_main_app_rest_template'),

    url(r'^data/get$', data_views.get_by_id,
        name='core_main_app_rest_data_get_by_id'),

    url(r'^data/get-full$', data_views.get_by_id_with_template_info,
        name='core_main_app_rest_data_get_by_id_with_template_info'),

    url(r'^data/download', data_views.download,
        name='core_main_app_rest_data_download'),

    url(r'^data/delete', data_views.delete,
        name='core_main_app_rest_data_delete'),

    url(r'^data/query', data_views.execute_query,
        name='core_main_app_rest_data_execute_query'),

    url(r'^data', data_views.data,
        name='core_main_app_rest_data'),

    url(r'^blob/download', blob_views.download,
        name='core_main_app_rest_blob_download'),

    url(r'^blob/upload', blob_views.upload,
        name='core_main_app_rest_blob_upload'),

    url(r'^blob/delete', blob_views.delete,
        name='core_main_app_rest_blob_delete'),

    url(r'^blob/list/delete', blob_views.delete_list,
        name='core_main_app_rest_blob_delete_list'),

    url(r'^blob/list', blob_views.list_all,
        name='core_main_app_rest_blob_list'),
]
