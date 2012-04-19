
from django.conf.urls import patterns, url

from albums.views import AlbumView


urlpatterns = patterns('',
    url(r'$', AlbumView.as_view(), name="albums-collection"),
)