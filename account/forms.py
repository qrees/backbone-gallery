from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _

from account.models import Profile


class BootstrapWidget(forms.Widget):
    pass


class BootstrapForm(forms.Form):

    def __unicode__(self):
        return self.as_bootstrap()

    def as_bootstrap(self):
        normal_row = '''
            <div class="control-group error" %(html_class_attr)s>
            <label class="control-label" for="inputError">%(label)s</label>
            <div class="controls">
            %(field)s
            </div>
            %(errors)s
            </div>
            '''
        return self._html_output(
            normal_row = normal_row,
            error_row = u'<span class="help-inline">%s</span>',
            row_ender = '</div>',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = False)



class RegisterForm(BootstrapForm):

    username = forms.CharField(required=True, max_length=255)
    email = forms.CharField(required=True, max_length=255)
    password1 = forms.CharField(required=True, label=_("Password"), widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, label=_("Repeat password"), widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if Profile.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("User with this name already exists")
        return self.cleaned_data['username']

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if Profile.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("User with this email already exists")
        return self.cleaned_data['email']

    def clean(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self._errors['password2'] = self._errors.get('password2', ErrorList())
            self._errors['password2'].append(_('Passwords do not match.'))
        return self.cleaned_data

    def save(self):
        profile = Profile.objects.create_account(
                password=self.cleaned_data['password1'],
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'])
        return profile

class LoginForm(BootstrapForm, AuthenticationForm):
    pass
