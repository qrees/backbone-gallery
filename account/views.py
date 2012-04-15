
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from account.forms import LoginForm, RegisterForm


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/register.html'


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def get_success_url(self):
        return reverse('user_page')
