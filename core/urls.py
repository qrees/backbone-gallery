from django.conf.urls import patterns, url
from core.views import jsreverse


urlpatterns = patterns('',
    url(r'^reverse\.js$', jsreverse, name="core-jsreverse"),
)