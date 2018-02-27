"""Url router for the REST API
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import core_main_app.rest.xsl_transformation.views as xslTransformationList_view
from core_main_app.rest.blob import views as blob_views
from core_main_app.rest.data import views as data_views
from core_main_app.rest.template import views as template_views
from core_main_app.rest.template_version_manager import views as template_version_manager_views

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

    url(r'^data/$', data_views.DataList.as_view(),
        name='core_main_app_rest_data_list'),

    url(r'^data/(?P<pk>\w+)/$', data_views.DataDetail.as_view(),
        name='core_main_app_rest_data_detail'),

    url(r'^data/download/(?P<pk>\w+)/$', data_views.DataDownload.as_view(),
        name='core_main_app_rest_data_download'),

    url(r'^data/get-full$', data_views.get_by_id_with_template_info,
        name='core_main_app_rest_data_get_by_id_with_template_info'),

    url(r'^blob/$', blob_views.BlobList.as_view(),
        name='core_main_app_rest_blob_list'),

    url(r'^blobs/delete/$', blob_views.BlobDeleteList.as_view(),
        name='core_main_app_rest_blob_delete_list'),

    url(r'^blob/(?P<pk>\w+)/$', blob_views.BlobDetail.as_view(),
        name='core_main_app_rest_blob_detail'),

    url(r'^blob/download/(?P<pk>\w+)/$', blob_views.BlobDownload.as_view(),
        name='core_main_app_rest_blob_download'),

    url(r'^xslt/$', xslTransformationList_view.XslTransformationList.as_view(),
        name='core_main_app_rest_xslt'),

    url(r'^xslt/transform/$', xslTransformationList_view.XslTransformationTransform.as_view(),
        name='core_main_app_rest_xslt_transform'),

    url(r'^xslt/(?P<pk>\w+)/$', xslTransformationList_view.XslTransformationDetail.as_view(),
        name='core_main_app_rest_xslt_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
