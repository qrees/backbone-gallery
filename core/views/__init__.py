from __future__ import absolute_import

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
