""" Url router for the main application
"""
import core_main_app.views.user.views as user_views
from django.conf.urls import url, include


urlpatterns = [
    url(r'^$', user_views.homepage, name='core_main_app_homepage'),

    url(r'^login', user_views.custom_login, name='core_main_app_login'),
    url(r'^logout', user_views.custom_logout, name='core_main_app_logout'),

    url(r'^rest/', include('core_main_app.rest.urls')),
    url(r'^data', user_views.data_detail, name='core_main_app_data_detail'),
]
