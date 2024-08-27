"""Url router for the REST API
"""

from django.urls import re_path

from core_main_app.rest.blob import views as blob_views
from core_main_app.rest.data import views as data_views
from core_main_app.rest.template import views as template_views

urlpatterns = [
    re_path(
        r"^template/(?P<pk>\w+)/download/$",
        template_views.TemplateDownload.as_view(),
        name="core_main_app_rest_template_download",
    ),
    re_path(
        r"^data/download/(?P<pk>\w+)/$",
        data_views.DataDownload.as_view(),
        name="core_main_app_rest_data_download",
    ),
    re_path(
        r"^blob/download/(?P<pk>\w+)/$",
        blob_views.BlobDownload.as_view(),
        name="core_main_app_rest_blob_download",
    ),
]
