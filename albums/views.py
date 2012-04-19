from albums.models import Album
from core.views import Collection


class AlbumView(Collection):
    model = Album
