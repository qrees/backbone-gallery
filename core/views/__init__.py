from __future__ import absolute_import
from django.template.base import Template

from core.views.collections import *


from django.conf import settings
from django.shortcuts import render_to_response
from django.utils import simplejson as json


def jsreverse(request):
    from django.core.urlresolvers import get_resolver, get_urlconf
    urlconf = get_urlconf()
    resolver = get_resolver(urlconf)
    d = {}
    fun_map = dict([(x[1][1], x[0]) for x in resolver.reverse_dict.items() if not isinstance(x[0], basestring)])
    name_map = dict([(x[1][1], x[0]) for x in resolver.reverse_dict.items() if isinstance(x[0], basestring)])

    for key in resolver.reverse_dict:
        if not isinstance(key, basestring):
            continue
        pattern_list = [{
            "pattern": p[1], "opts": [o[0] for o in p[0]]
        } for p in resolver.reverse_dict.getlist(key) if p[1] in fun_map and getattr(fun_map[p[1]], 'expose', False)]
        if pattern_list:
            d[key] = pattern_list
    return render_to_response("core/django_reverse.js",
            {"reverse_dict": json.dumps(d), "settings": settings},
        mimetype="text/javascript",)

import json
from django.template import loader
from django.conf import settings
from django import http
import os.path
import os

def jstemplates(request):
    if not 'path' in request.GET:
        return http.HttpResponseBadRequest('Missing path query')
    path = request.GET['path']
    context = RequestContext(request=request)
    templates = {}
    for lookup in settings.JS_TEMPLATES:
        joined = os.path.normpath(os.path.join(lookup, path))
        prefix = os.path.commonprefix([lookup, joined])
        if not prefix.startswith(lookup):
            return http.HttpResponseBadRequest('Invalid path query')
        if not os.path.isdir(joined):
            return http.HttpResponseNotFound('Template path was not found')
        files = os.listdir(joined)
        for file in files:
            tmpl_path = os.path.join(joined, file)
            with open(tmpl_path) as tmpl_file:
                tmpl = Template(tmpl_file.read())
                templates[file] = tmpl.render(context)
    json_dump = json.dumps(templates)
    context.update({'templates': json_dump})
    return render_to_response("core/jquery_templates.js", context_instance=context, mimetype="text/javascript")