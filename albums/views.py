from django.views.generic.base import TemplateView
from albums.models import Album
from core.decorators import view_decorator
from core.views import ResourceView


class AlbumPage(TemplateView):
    template_name = "albums/main.html"


def expose(view):
    view.expose = True
    return view


@view_decorator(expose)
class AlbumView(ResourceView):
    model = Album
