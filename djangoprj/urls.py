from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^', include('apps.home.urls')),
    url(r'^account/', include('apps.account.urls')),
    url(r'^query/', include('apps.query.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)
