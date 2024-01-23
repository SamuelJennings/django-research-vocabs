from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import URLField
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase


class ConceptField(URLField):
    """A URL field that stores a URI for a SKOS Concept. The field expects a scheme parameter which takes accepts a
    valid ConceptSceme object. The field validates that the URI is a member of the ConceptScheme and provides a ChoiceField
    populated by concepts in the scheme."""

    def __init__(self, scheme, *args, **kwargs):
        self.scheme = scheme
        kwargs["choices"] = self.scheme.choices
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["scheme"] = self.scheme
        return name, path, args, kwargs

    def get_choice_data(self):

        # get DB value
        db_value = self.value_from_object(self.model_instance)

        # get the concept from the scheme
        return self.scheme.get_concept_meta(db_value)


class TaggableConcepts(GenericRelation):
    def __init__(self, *args, **kwargs):
        kwargs["to"] = "research_vocabs.TaggedConcept"
        super().__init__(*args, **kwargs)
