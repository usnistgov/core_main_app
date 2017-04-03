""" Url router for the main application
"""
import core_main_app.views.user.views as user_views
from django.conf.urls import url, include


urlpatterns = [
    url(r'^rest/', include('core_main_app.rest.urls')),
    url(r'^data', user_views.data_detail, name='core_main_app_data_detail'),
]
