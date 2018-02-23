from django.shortcuts import render_to_response
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import InputUrlForm
from .parser import HTMLKeywordsParser


class FormInputView(FormView):

    form_class = InputUrlForm
    template_name = 'keywords/index.html'

    success_url = reverse_lazy('index')

    def form_valid(self, form):

        url = form.cleaned_data['url']

        parser = HTMLKeywordsParser(url)

        context = {
            'form': form,
            'result': parser.get_result()
        }

        return render_to_response(self.template_name, context)
