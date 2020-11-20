"""Url router for the REST API
"""
from django.urls import re_path

from core_main_app.rest.template import views as template_views

urlpatterns = [
    re_path(
        r"^template/(?P<pk>\w+)/download/$",
        template_views.TemplateDownload.as_view(),
        name="core_main_app_rest_template_download",
    ),
]
