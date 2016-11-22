""" Url router for the main application
"""
from django.conf.urls import url, include

urlpatterns = [
    url(r'^rest/', include('core_main_app.rest.urls')),
]
