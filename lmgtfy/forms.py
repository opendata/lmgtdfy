from django import forms

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
            'search_field',
            CleanSubmitButton('submit', 'Data search')
        )

    search_field = forms.URLField(label='http://example.gov')
