from neapolitan.views import CRUDView

from .forms import ExampleForm
from .models import TestModel


class ExampleCRUDView(CRUDView):
    model = TestModel
    form_class = ExampleForm
    fields = ["name", "concept_label", "concept_builder", "m2m"]
    # success_url = reverse_lazy("example_form")
