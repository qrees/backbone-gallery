# Create your views here.
from django.conf import settings
from django.http import HttpResponse
from django.template.context import RequestContext
from django.views.generic.edit import FormView
import jinja2

from account.forms import LoginForm


template_dirs = getattr(settings,'TEMPLATE_DIRS')
default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dirs))


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    def render_to_response(self, context, **response_kwargs):
        template = env.select_template(self.get_template_names())
        context = RequestContext(self.request, context)
        context = context.update({'request': self.request})
        rendered = template.render(**context)
        return HttpResponse(
            rendered,
            **response_kwargs
        )