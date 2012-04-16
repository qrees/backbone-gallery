from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
import account.urls

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include(account.urls)),
    url(r'^auth/', include('social_auth.urls')),
)
