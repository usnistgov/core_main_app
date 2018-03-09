from django.conf.urls import url, include
from django.contrib import admin
from core_main_app import urls as core_main_app_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
] + core_main_app_urls.urlpatterns
