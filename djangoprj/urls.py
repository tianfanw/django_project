from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apps.home.views.index', name='index'),
    url(r'^home/', include('apps.home.urls')),
    url(r'^account/', include('apps.account.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
