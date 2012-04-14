__author__ = 'qrees'

from django import forms
from django.contrib.auth.forms import AuthenticationForm

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

class LoginForm(BootstrapForm, AuthenticationForm):
    pass