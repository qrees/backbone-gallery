from django.conf.urls import patterns, url
from core.views import jsreverse, jstemplates


urlpatterns = patterns('',
    url(r'^reverse\.js$', jsreverse, name="core-jsreverse"),
    url(r'^templates\.js$', jstemplates, name="core-jstemplates"),
)