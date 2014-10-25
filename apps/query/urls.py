from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.query.views',
    # Examples:
    url(r'^search', 'search', name='search'),
    # url(r'^results', 'results', name='results'),
    # url(r'^admin/', include(admin.site.urls)),
)
