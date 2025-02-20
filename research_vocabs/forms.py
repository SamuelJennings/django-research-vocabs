from django import forms
from django.utils.safestring import mark_safe

from research_vocabs.core import Concept as BaseConcept
from research_vocabs.models import Concept


class TaggableConceptFormMixin:
    """When TaggableConceptFormMixin is used in a form, the form will automatically detect KeywordField fields and clean them and add them to a designated keyword field on the model."""

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super().__init__(*args, **kwargs)
        # Ensure taggable_field_name and taggable_fields are defined in Meta
        if not hasattr(self.Meta, "taggable_field_name") or not hasattr(self.Meta, "taggable_fields"):
            raise AttributeError("Meta class must define 'taggable_field_name' and 'taggable_fields'.")

        self.taggable_field_name = self.Meta.taggable_field_name
        self.taggable_fields = self.Meta.taggable_fields

        # Initialize the hidden field for the M2M relationship
        # self.fields[self.taggable_field_name] = forms.ModelMultipleChoiceField(
        #     widget=forms.HiddenInput, queryset=Concept.objects.all(), required=False
        # )

        if self.instance and self.instance.pk:
            self.populate_concept_fields()

    def populate_concept_fields(self):
        """Make sure the correct form fields are populated with the correct concepts."""
        concepts = getattr(self.instance, self.taggable_field_name).all()
        for fname in self.taggable_fields:
            f_vocab = self.fields[fname].vocabulary
            # this will produce wrong results if multiple vocabularies have a term with the same name
            self.initial[fname] = [c.name for c in concepts if c.name in f_vocab.values]

    def clean(self):
        """Clean all fields."""
        super().clean()
        self.concepts = self._clean_concepts()

    def _clean_concepts(self):
        """Clean the keywords."""
        concepts = []
        for fname in self.taggable_fields:
            value = self.cleaned_data.get(fname)
            if not value:
                continue
            if isinstance(value, BaseConcept):
                value = [value]

            concepts.extend(value)
        return concepts

    def _save_m2m(self):
        """Save the cleaned data to the model."""
        super()._save_m2m()
        self.update_taggable_concepts()

    def update_taggable_concepts(self):
        concepts = []
        for c in self.concepts:
            obj, created = Concept.add_concept(c)
            concepts.append(obj)
        getattr(self.instance, self.taggable_field_name).add(*concepts)


class ConceptFieldMixin:
    def __init__(self, vocabulary, *args, **kwargs):
        self.vocabulary = vocabulary()
        kwargs["choices"] = self.vocabulary.choices

        kwargs["label"] = kwargs.get("label", self.vocabulary.label())
        if not kwargs.get("help_text"):
            scheme_uri = self.vocabulary.scheme().URI
            label = self.vocabulary.label()
            kwargs["help_text"] = mark_safe(  # noqa: S308
                f"Select terms from the <a href='{scheme_uri}' target='_blank'>{label}</a> controlled vocabulary."  # noqa: S608
            )
        super().__init__(*args, **kwargs)


class ConceptField(ConceptFieldMixin, forms.ChoiceField):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        return self.vocabulary.get_concept(value)


class MultiConceptField(ConceptFieldMixin, forms.MultipleChoiceField):
    def to_python(self, value):
        if not value:
            return []
        return [self.vocabulary.get_concept(v) for v in value]
