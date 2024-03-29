from django.views.generic.base import TemplateView
from albums.forms import FileForm
from albums.models import Album, File
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


@view_decorator(expose)
class FileView(ResourceView):
    create_form = FileForm
    model = File
