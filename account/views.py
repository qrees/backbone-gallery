from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import FormView

from account.forms import LoginForm, RegisterForm


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        user = form.save()
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('account-login')


class LogoutView(RedirectView):
    def get_redirect_url(self, **kwargs):
        return reverse('account-login')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        # TODO : handle "next" vlaue
        return reverse('account-page')


class AccountView(TemplateView):
    template_name = "account/page.html"

account_view = login_required(AccountView.as_view())