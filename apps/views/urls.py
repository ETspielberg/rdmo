from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', views, name='views'),
    url(r'^export/xml/$', views_export_xml, name='views_export_xml'),
    url(r'^export/(?P<format>[a-z]+)/$', views_export, name='views_export'),
]
