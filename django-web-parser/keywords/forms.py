from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class InputUrlForm(forms.Form):

    url = forms.URLField(
        label="Podaj adres URL"
    )

    ignore_script = forms.BooleanField(
        label='Ignoruj wystąpienia w kodzie JavaScript',
        required=False,
        initial=True
    )

    def __init__(self, *args, **kwargs):
        super(InputUrlForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Wyślij'))
