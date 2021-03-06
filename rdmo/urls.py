from django.conf.urls import include, url
from django.contrib import admin

from apps.core.views import home, i18n_switcher

urlpatterns = [
    url(r'^$', home, name='home'),

    # apps
    url(r'^account/', include('apps.accounts.urls')),
    url(r'^domain/', include('apps.domain.urls')),
    url(r'^options/', include('apps.options.urls')),
    url(r'^projects/', include('apps.projects.urls')),
    url(r'^questions/', include('apps.questions.urls')),
    url(r'^tasks/', include('apps.tasks.urls')),
    url(r'^conditions/', include('apps.conditions.urls')),
    url(r'^views/', include('apps.views.urls')),

    # REST api
    url(r'^api/domain/', include('apps.domain.urls_api', namespace='domain')),
    url(r'^api/options/', include('apps.options.urls_api', namespace='options')),
    url(r'^api/projects/', include('apps.projects.urls_api', namespace='projects')),
    url(r'^api/questions/', include('apps.questions.urls_api', namespace='questions')),
    url(r'^api/tasks/', include('apps.tasks.urls_api', namespace='tasks')),
    url(r'^api/conditions/', include('apps.conditions.urls_api', namespace='conditions')),
    url(r'^api/views/', include('apps.views.urls_api', namespace='views')),

    # langage switcher
    url(r'^i18n/([a-z]{2})/$', i18n_switcher, name='i18n_switcher'),

    url(r'^admin/', include(admin.site.urls)),
]
