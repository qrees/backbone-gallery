from django.conf.urls import patterns, url

from account.views import LoginView, RegisterView, account_view, LogoutView


urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name="account-login"),
    url(r'^logout/$', LogoutView.as_view(), name="account-logout"),
    url(r'^register/$', RegisterView.as_view(), name="account-register"),
    url(r'$', account_view, name="account-page")
)