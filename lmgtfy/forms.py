from urlparse import urlparse
from django import forms
from django.core import validators

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from lmgtfy.helpers import CleanSubmitButton


class MainForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            'domain',
            CleanSubmitButton('submit', 'Search Data')
        )

    domain = forms.CharField(label='example.gov', required=True)

    def clean(self):
        cleaned_data = super(MainForm, self).clean()
        domain_string = cleaned_data.get('domain', '')
        if not (domain_string.startswith('http://') or domain_string.startswith('https://')):
            domain_string = 'http://%s' % domain_string
        validator = validators.URLValidator()
        try:
            validator(domain_string)
        except:
            raise forms.ValidationError('Please enter a valid URL.')
        cleaned_data['domain_base'] = urlparse(domain_string).netloc
        return cleaned_data
