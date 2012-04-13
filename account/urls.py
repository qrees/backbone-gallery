__author__ = 'qrees'

from django.conf.urls import patterns, url
from django.contrib.auth.views import login

urlpatterns = patterns('',
    url(r'^login/$', login, kwargs={'template_name': 'account/login.html'}),

)