from django.conf.urls import patterns, include, url
from django.contrib import admin

import account.urls
import albums.urls
import core.urls

admin.autodiscover()

urlpatterns = patterns('',

    url(r'', include(core.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include(account.urls)),
    url(r'^albums/', include(albums.urls)),
    url(r'^auth/', include('social_auth.urls')),
)
