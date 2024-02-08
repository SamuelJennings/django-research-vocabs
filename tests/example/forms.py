from research_vocabs.forms import KeywordChoiceField, KeywordModelForm

from .choices import ISC2020, MyMaterialsScheme, SimpleLithology
from .models import TestModel


class ExampleForm(KeywordModelForm):
    # single_choice = KeywordChoiceField(scheme=SimpleLithology)
    # multi_choice = KeywordChoiceField(scheme=SimpleLithology)

    model_choice = KeywordChoiceField(scheme=SimpleLithology)

    class Meta:
        model = TestModel
        fields = ["name", "concept", "model_choice"]  # noqa: RUF012

        taggable_schemes = {  # noqa: RUF012
            "age": {"scheme": ISC2020},
            "material": {"scheme": MyMaterialsScheme, "multiple": True},
        }

        taggable_field = "tagged_concepts"  # noqa: RUF012
