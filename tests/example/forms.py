# from test import GeologicUnit


from research_vocabs.forms import KeywordChoiceField, KeywordModelForm

from .choices import BoreholeDrilling, SimpleLithology
from .models import TestModel


class ExampleForm(KeywordModelForm):
    # single_choice = KeywordChoiceField(scheme=SimpleLithology)
    # multi_choice = KeywordMultiChoiceField(scheme=SimpleLithology)

    model_choice = KeywordChoiceField(scheme=SimpleLithology)

    class Meta:
        model = TestModel
        fields = ["name", "concept", "model_choice"]  # noqa: RUF012

        taggable_schemes = {  # noqa: RUF012
            "lith": {"scheme": SimpleLithology},
            "drill": {"scheme": BoreholeDrilling, "multiple": True},
        }

        taggable_field = "tagged_concepts"  # noqa: RUF012
