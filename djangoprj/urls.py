from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^', include('apps.home.urls')),
    # url(r'^account/', include('apps.account.urls')),
    # url(r'^search', include('apps.query.urls')),
    url(r'^$', 'myapp.views.index', name='index'),
    url(r'^login$', 'myapp.views.login', name='login'),
    url(r'^register$', 'myapp.views.register', name='register'),
    url(r'^logout$', logout, kwargs={'next_page':'/'}, name="logout"),
    url(r'^search', 'myapp.views.search', name='search'),
    # url(r'^admin/', include(admin.site.urls)),
)
