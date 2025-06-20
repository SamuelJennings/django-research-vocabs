from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Layout, Submit
from django import forms

from research_vocabs.forms import ConceptField, MultiConceptField, TaggableConceptFormMixin

from .models import TestModel
from .vocabularies import ISC2020, SimpleLithology


class ExampleForm(TaggableConceptFormMixin, forms.ModelForm):
    single_choice = ConceptField(vocabulary=SimpleLithology)
    multi_choice = MultiConceptField(vocabulary=ISC2020)

    class Meta:
        model = TestModel
        fields = ["name", "single_choice", "multi_choice"]
        taggable_field_name = "taggable_concepts"
        taggable_fields = ["single_choice", "multi_choice"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name",
            HTML("<p>I'm a standard Django charfield that stores a single vocabulary terms</p>"),
            HTML(
                "<h5>Keywords:</h5><p>These are seperate fields that will all stores their values in a Django related object.</p>"
            ),
            "single_choice",
            "multi_choice",
            ButtonHolder(Submit("submit", "Submit")),
        )


class AdminForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = "__all__"

    def full_clean(self):
        super().full_clean()
