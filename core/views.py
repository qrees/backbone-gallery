import importlib
from django.template import loader
from django.template.context import RequestContext
from django.views.generic.base import View
import json
import mimeparse


class CollectionMixin(object):

    def get_context_data(self):
        return {}

    pk_field = 'id'
    model = None


class Presenter(object):
    def __init__(self, view, mimetype):
        self.view = view
        self.mimetype = mimetype


class JSONPresenter(Presenter):

    def render(self, context):
        return json.dumps(context)

class TemplatePresenter(Presenter):

    def render(self, context):
        template_name = self.view.get_template_name()
        req_context = RequestContext(self.view.request)
        req_context.update(context)
        loader.render_to_string(template_name, context_instance=req_context)


conf = {
    'formats': {
        'application/json': 'core.views.JSONPresenter',
        'text/html': 'core.views.TemplatePresenter'
    }
}

def import_class(path):
    modpath, clsname = path.rsplit('.', 1)
    mod = importlib.import_module(modpath)
    return getattr(mod, clsname)

def get_format(request, formats=None, default_format=None):
    if formats is None:
        formats = conf['formats'].keys()
    accepted = request.META.get('HTTP_ACCEPT', '*/*')
    best_format = mimeparse.best_match(formats, accepted)
    return best_format

def get_presenter(format):
    presenter_name = conf['formats'][format]
    cls = import_class(presenter_name)
    return cls


class ViewMixin(object):
    template_name = None
    
    def get_context_data(self):
        return {}

    def get_template_name(self):
        return self.template_name

    def get_presenter(self, default_format=None):
        mimetype = get_format(self.request)
        presenter_cls = get_presenter(mimetype)
        presenter = presenter_cls(view=self, mimetype=mimetype)
        return presenter

    def render_to_response(self):
        import ipdb
        ipdb.set_trace()
        context = self.get_context_data()
        presenter = self.get_presenter()
        return presenter.render(context)


class Collection(CollectionMixin, ViewMixin, View):

    def get(self, request, **kwargs):
        return self.render_to_response()