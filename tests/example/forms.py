from django import forms

from research_vocabs.forms import KeywordChoiceField, KeywordModelForm

from .models import TestModel
from .vocabularies import ISC2020, CustomMaterials, SimpleLithology


class ExampleForm(KeywordModelForm):
    # single_choice = KeywordChoiceField(scheme=SimpleLithology)
    # multi_choice = KeywordChoiceField(scheme=SimpleLithology)

    standard = KeywordChoiceField(scheme=SimpleLithology())
    grouped = KeywordChoiceField(scheme=SimpleLithology())

    class Meta:
        model = TestModel
        fields = ["name", "concept_label", "standard", "grouped"]

        taggable_schemes = {
            "age": {"scheme": ISC2020()},
            "material": {"scheme": CustomMaterials(), "multiple": True},
        }

        taggable_field = "tagged_concepts"


class AdminForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = "__all__"

    def full_clean(self):
        super().full_clean()
