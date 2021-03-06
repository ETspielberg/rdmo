from django.conf.urls import url

from .views import options, options_export, options_export_xml

urlpatterns = [
    url(r'^$', options, name='options'),
    url(r'^export/xml/$', options_export_xml, name='options_export_xml'),
    url(r'^export/(?P<format>[a-z]+)/$', options_export, name='options_export'),
]
