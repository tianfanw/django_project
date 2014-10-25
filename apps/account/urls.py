from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout
 
# urlpatterns = patterns('apps.accounts.views',
#     url(r'^register/$', 'register', name="accounts_register")
# )
urlpatterns = patterns('apps.account.views',
  url(r'^login$', 'login', name='login'),
  url(r'^register$', 'register', name='register'),
  url(r'^logout$', logout, kwargs={'next_page':'/'}, name="logout"),
)