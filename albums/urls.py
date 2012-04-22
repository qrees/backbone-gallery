
from django.conf.urls import patterns, url

from albums.views import AlbumView, AlbumPage

uuid = r'(?P<uuid>[0-9a-z]{32})'

urlpatterns = patterns('',
    url(r'^$', AlbumPage.as_view(), name="albums"),
    url(r'^list/$', AlbumView.as_view(), name="albums-list"),
    url(r'^item/%s/$' % uuid, AlbumView.as_view(), name="albums-item"),
)