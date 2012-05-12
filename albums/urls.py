
from django.conf.urls import patterns, url

from albums.views import AlbumView, AlbumPage, FileView

uuid = r'(?P<uuid>[0-9a-z]{32})'

urlpatterns = patterns('',
    url(r'^$', AlbumPage.as_view(), name="albums"),
    url(r'^albums/$', AlbumView.as_view(), name="albums-list"),
    url(r'^albums/%s/$' % uuid, AlbumView.as_view(), name="albums-item"),
    url(r'^files/$', FileView.as_view(), name="files-list"),
    url(r'^files/%s/$' % uuid, FileView.as_view(), name="files-item"),
)