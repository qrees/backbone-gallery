from django.conf.urls import patterns, url

from account.views import LoginView, RegisterView


urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name="account-login"),
    url(r'^register/$', RegisterView.as_view(), name="account-register"),


)