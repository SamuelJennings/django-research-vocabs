from django import forms

from research_vocabs.models import Concept, TaggedConcept


class KeywordFieldBase:
    def __init__(self, scheme="", *args, **kwargs):
        """Initialize the field."""
        self.scheme = scheme

        super().__init__(*args, **kwargs)
        self.choices = self.scheme.choices

    def clean(self, value):
        """Clean the field."""
        value = super().clean(value)

        if not isinstance(value, list):
            value = [value]

        # for value in value:
        #     if isinstance(value, Concept):
        #         continue
        # value, created = Concept.add_concept(URI=value, scheme=self.scheme)

        return [Concept.add_concept(URI=value, scheme=self.scheme)[0] for value in value]


class KeywordChoiceField(KeywordFieldBase, forms.ChoiceField):
    """A field that is used to collect controlled keywords and add them to a designated keyword field on the model."""


class KeywordMultiChoiceField(KeywordFieldBase, forms.MultipleChoiceField):
    """A field that is used to collect multiple controlled keywords and add them to a designated keyword field on the model."""


class KeywordFormMixin:
    """When KeywordFormMixin is used in a form, the form will automatically detect KeywordField fields and clean them and add them to a designated keyword field on the model."""

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super().__init__(*args, **kwargs)
        self.taggable_schemes = getattr(self.Meta, "taggable_schemes", {})
        self.taggable_field = getattr(self.Meta, "taggable_field", "tagged_concepts")

        # make sure the model has a taggable field
        if not hasattr(self.Meta.model, self.taggable_field):
            raise AttributeError(f"Model {self.Meta.model} does not have a taggable field {self.taggable_field}")

        if self.taggable_schemes:
            for field_name, opts in self.taggable_schemes.items():
                field_class = KeywordMultiChoiceField if opts.get("multiple") else KeywordChoiceField
                self.fields[field_name] = field_class(scheme=opts["scheme"])

        self.keyword_fields = [name for name, f in self.fields.items() if isinstance(f, KeywordFieldBase)]

    def clean(self):
        """Clean all fields."""
        super().clean()
        self.cleaned_data[self.taggable_field] = self._clean_keywords()

    def _clean_keywords(self):
        """Clean the keywords."""
        keywords = []
        for fname in self.keyword_fields:
            for value in self.cleaned_data[fname]:
                keywords.append(value)
        return keywords


class KeywordForm(KeywordFormMixin, forms.Form):
    pass


class KeywordModelForm(KeywordFormMixin, forms.ModelForm):
    # @transaction.atomic
    # def save(self, commit=True):
    #     return super().save(commit)

    def _save_m2m(self):
        """Save the cleaned data to the model."""
        super()._save_m2m()
        keywords = []
        for concept in self.cleaned_data[self.taggable_field]:
            tag = TaggedConcept(content_object=self.instance, concept=concept)
            # tag.save()
            keywords.append(tag)

        getattr(self.instance, self.taggable_field).add(*keywords, bulk=False)
