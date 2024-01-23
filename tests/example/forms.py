# from test import GeologicUnit


from django.forms import ModelChoiceField

from research_vocabs.forms import KeywordModelChoiceField, KeywordModelForm
from research_vocabs.models import Concept

from .choices import BoreholeDrilling, SimpleLithology
from .models import ExampleModel


class ExampleForm(KeywordModelForm):
    # single_choice = KeywordChoiceField(scheme=SimpleLithology)
    # multi_choice = KeywordMultiChoiceField(scheme=SimpleLithology)

    model_choice = KeywordModelChoiceField(scheme=SimpleLithology)

    class Meta:
        model = ExampleModel
        fields = ["name", "concept"]  # noqa: RUF012

        taggable_schemes = {  # noqa: RUF012
            "lith": {"scheme": SimpleLithology},
            "drill": {"scheme": BoreholeDrilling, "multiple": True},
        }

        taggable_field = "keywords"
