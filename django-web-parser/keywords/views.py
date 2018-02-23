from django.urls import reverse_lazy
from django.views.generic import FormView

from .exceptions import NoKeywordsException, BadURLException
from .forms import InputUrlForm
from .parser import HTMLKeywordsParser


class FormInputView(FormView):

    form_class = InputUrlForm
    template_name = 'keywords/index.html'

    success_url = reverse_lazy('index')

    def form_valid(self, form):

        return_context = self.get_context_data(form=form)

        url = form.cleaned_data['url']
        ignore_script = form.cleaned_data['ignore_script']

        try:
            parser = HTMLKeywordsParser(url)

        except BadURLException:
            return_context.update({
                'error': 'Nie udało się pobrać zawartości danej strony.'
            })
            # stop further processing
            return self.render_to_response(return_context)

        try:
            parser_result = parser.get_result(ignore_script)

        except NoKeywordsException:
            return_context.update({
                'error': 'Podana strona nie zawiera żadnych słów kluczowych'
            })

        else:
            return_context.update({
                'result': parser_result
            })

        return self.render_to_response(return_context)
