import importlib
from django.core import serializers
from django.db.models.fields.files import FieldFile

from django.http import HttpResponse
from django.utils import simplejson
from django.db.models.query import QuerySet
from django.db.models import Model
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
    content_type = None
    def __init__(self, view, mimetype):
        self.view = view
        self.mimetype = mimetype

    def response(self, **kwargs):
        kwargs['content_type'] = self.content_type
        return HttpResponse(**kwargs)

    def not_acceptable(self, **kwargs):
        kwargs['status'] = 406
        return self.response(**kwargs)

from django.forms.models import model_to_dict

class MetaSerializable(type):

    def __new__(meta, classname, bases, classDict):
        return type.__new__(meta, classname, bases, classDict)

    def __instancecheck__(self, instance):
        return hasattr(instance, 'as_dict')


class Serializable(object):
    __metaclass__ = MetaSerializable


class HandleQuerySets(simplejson.JSONEncoder):
    """ simplejson.JSONEncoder extension: handle querysets """

    def model_to_dict(self, instance):
        return {
            'fields': instance.as_dict()
        }

    def default(self, obj):
        if isinstance(obj, (QuerySet, list, tuple)):
            return [self.default(x) for x in obj]
        if isinstance(obj, Serializable):
            return self.model_to_dict(obj)
        if isinstance(obj, FieldFile):
            return obj.url
        return simplejson.JSONEncoder.default(self, obj)


class JSONPresenter(Presenter):
    dehydrate = True
    content_type = 'application/json; charset=utf-8'

    def render(self, context, **kwargs):
        if not isinstance(self.view, DehydrateViewMizin):
            return self.not_acceptable(content='', **kwargs)
        context = self.view.dehydrate_context(context)
        #payload = serializers.serialize('json', context)
        payload = json.dumps(context, cls=HandleQuerySets)
        return HttpResponse(content=payload, **kwargs)


class TemplatePresenter(Presenter):
    dehydrate = False
    content_type = 'text/html; charset=utf-8'

    def render(self, context, **kwargs):
        if not isinstance(self.view, TemplateViewMixin):
            return self.not_acceptable(content='', **kwargs)
        template_name = self.view.get_template_name()
        if template_name is None:
            return self.not_acceptable(content='', **kwargs)
        req_context = RequestContext(self.view.request)
        req_context.update(context)
        payload = loader.render_to_string(template_name, context_instance=req_context)
        return HttpResponse(content=payload, **kwargs)


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


class DehydrateViewMizin(object):
    def dehydrate_context(self, context):
        return context

class TemplateViewMixin(object):
    template_name = None

    def get_template_name(self):
        return self.template_name


class ViewMixin(DehydrateViewMizin, TemplateViewMixin):

    def get_context_data(self):
        return {}

    def get_presenter(self, default_format=None):
        mimetype = get_format(self.request, default_format)
        presenter_cls = get_presenter(mimetype)
        presenter = presenter_cls(view=self, mimetype=mimetype)
        return presenter

    def render_to_response(self, context, **kwargs):
        presenter = self.get_presenter()
        return presenter.render(context, **kwargs)

    def response_not_allowed(self):
        return self.render_to_response({}, status=405)


class Collection(CollectionMixin, ViewMixin, View):
    create_form = None

    def get_model_queryset(self):
        return self.model.objects.all()

    def get_instance_kwargs(self):
        return {'pk':self.kwargs[self.pk_field]}

    def get_model_instance(self):
        qs = self.get_model_queryset()
        return qs.get(**self.get_instance_kwargs())

    def get_list_context(self, qs):
        return qs

    def get_item_context(self, item):
        return [item]

    def get_item(self):
        item = self.get_model_instance()
        return self.render_to_response(self.get_item_context(item))

    def get_list(self):
        qs = self.get_model_queryset()
        return self.render_to_response(self.get_list_context(qs))

    def get(self, request, **kwargs):
        '''
            If object id is given in url return single object.
            Otherwise return list of objects from this collection.
        '''
        if self.pk_field in self.kwargs:
            return self.get_item()
        else:
            return self.get_list()

    def create_form_valid(self, form):
        instance = form.save()
        return self.render_to_response(self.get_item_context(instance))

    def extract_errors(self, form):
        error_list = []
        for field_name, val in form.errors.items():
            error_list.append((field_name, val[0]))
        return error_list

    def create_form_invalid(self, form):
        errors = self.extract_errors(form)
        return self.render_to_response({
            'errors': errors
        }, status=400)

    def get_create_form_kwargs(self):
        return {
            'data': self.request.POST,
            'files': self.request.FILES
        }

    def process_create_form(self):
        if self.create_form is None:
            return self.response_not_allowed()
        form_class = self.create_form
        form = form_class(**self.get_create_form_kwargs())
        if form.is_valid():
            return self.create_form_valid(form)
        else:
            return self.create_form_invalid(form)

    def post(self, request, **kwargs):
        '''
            Create object in collection
        '''
        if self.pk_field in self.kwargs:
            return self.response_not_allowed()
        return self.process_create_form()

class ResourceView(Collection):
    pk_field = 'uuid'

    def get_instance_kwargs(self):
        return {'uuid':self.kwargs[self.pk_field]}