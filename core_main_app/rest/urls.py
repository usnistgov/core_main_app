"""Url router for the REST API
"""
from django.conf.urls import url
from core_main_app.rest.template import views as template_views
from core_main_app.rest.template_version_manager import views as template_version_manager_views
from core_main_app.rest.data import views as data_views

urlpatterns = [
    url(r'^template/version/download$', template_views.download,
        name='core_main_app_rest_template_download'),

    url(r'^template_version_manager/select/all/global$', template_version_manager_views.get_all_globals,
        name='core_main_app_rest_template_version_manager_get_all_globals'),

    url(r'^template-version-manager', template_version_manager_views.template_version_manager,
        name='core_main_app_rest_template_version_manager'),

    url(r'^template', template_views.template,
        name='core_main_app_rest_template'),

    url(r'^data/get$', data_views.get_by_id,
        name='core_main_app_rest_data_get_by_id'),

    url(r'^data', data_views.data,
        name='core_main_app_rest_data'),
]
