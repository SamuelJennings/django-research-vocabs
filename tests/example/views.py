from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView

from .forms import ExampleForm
from .models import TestModel


class ExampleFormView(CreateView):
    model = TestModel
    form_class = ExampleForm
    template_name = "test_form.html"
    success_url = "."
