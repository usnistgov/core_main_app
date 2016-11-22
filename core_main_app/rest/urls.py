"""Url router for the REST API
"""
from django.conf.urls import url
from .template import views as template_views


urlpatterns = [
    url(r'^template/download$', template_views.download,
        name='core_main_app_rest_template_download'),
]
