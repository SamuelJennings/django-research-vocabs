from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import CharField, Field, URLField
from django.utils.translation import gettext as _

from research_vocabs.core import Concept


class MissingConceptSchemeError(Exception):
    """Raised when a concept scheme is not passed as an argument to the ConceptField class."""

    msg = "ConceptField requires a ConceptScheme object to be passed as an argument."

    # def __init__(self):
    # super().__init__("ConceptField requires a ConceptScheme object to be passed as an argument.")


class BaseConceptField(Field):
    """
    A custom field class that stores vocabulary concepts as a fully qualified URI. The concept scheme is passed as an argument during the initialization of the class.

    Attributes:
        scheme (ConceptScheme): The concept scheme that this field belongs to.

    Methods:

        get_choice_data(): Returns the concept metadata from the scheme using the DB value.
    """

    description = _("A concept within the %(vocabulary)s vocabulary.")

    def __init__(self, include_only: list = None, *args, **kwargs):
        """
        Initializes the ConceptField with the given scheme. The scheme's choices are also set as the choices for this field.

        Args:
            scheme (ConceptScheme): The concept scheme that this field belongs to.
        """
        self.vocabulary = kwargs.pop("vocabulary", None)
        if not self.vocabulary:
            raise MissingConceptSchemeError

        self.scheme = self.vocabulary(include_only=include_only)

        # vocab_registry.register(self.scheme)

        kwargs["choices"] = list(self.scheme.choices)
        kwargs["verbose_name"] = kwargs.get("verbose_name", self.scheme.scheme().label())
        kwargs["max_length"] = len(max(self.scheme.choices, key=lambda x: len(x[0]))[0])

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        """Used to recreate the field."""
        name, path, args, kwargs = super().deconstruct()
        kwargs["vocabulary"] = self.vocabulary
        kwargs.pop("choices", None)
        return name, path, args, kwargs

    def get_choice_data(self):
        """
        Returns the concept metadata from the scheme using the DB value.

        Returns:
            dict: A dictionary containing the concept metadata.
        """
        # get DB value
        db_value = self.value_from_object(self.model_instance)

        # get the concept from the scheme
        return self.scheme.get_concept_meta(db_value)

    def get_default_value(self):
        """
        Returns the default value for the field.

        Returns:
            str: The default value for the field.
        """
        return self.scheme.default

    def contribute_to_class(self, cls, name, **kwargs):
        """
        Adds the field to the class and sets the model instance.

        Args:
            cls (Model): The model class to which the field is being added.
            name (str): The name of the field.
        """
        super().contribute_to_class(cls, name, **kwargs)
        # auto add the vocab to the class
        setattr(cls, f"{name}_vocab", self.scheme)

    def get_prep_value(self, value):
        """
        Converts the Concept object to a name value.
        """
        if value is None:
            return value

        elif isinstance(value, Concept):
            return value.name

        return value

    def to_python(self, value):
        """
        Converts the URI value to a Concept object.
        """
        if isinstance(value, Concept):
            return value

        if value is None:
            return value

        return Concept(value, self.scheme)

    def validate(self, value, model_instance):
        """
        Validates the field value.
        """
        if value is None:
            return

        if not isinstance(value, Concept):
            raise ValueError(f"{value} is not a Concept object.")

        super().validate(value.name, model_instance)


class ConceptURIField(BaseConceptField, URLField):
    """
    A field that stores vocabulary concepts as a fully qualified URI.
    """


class ConceptField(BaseConceptField, CharField):
    """
    A field that stores vocabulary concepts as a simple text value.
    """


class TaggableConcepts(GenericRelation):
    """
    A custom field class that extends the GenericRelation class. This class is used to create a generic
    relation to the "research_vocabs.TaggedConcept" model. This allows the model that has this field to
    have a set of tagged concepts associated with it.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the TaggableConcepts field with a relation to the "research_vocabs.TaggedConcept" model.
        """
        kwargs["to"] = "research_vocabs.Concept"
        self.taggable_concepts = kwargs.pop("taggable_concepts", None)

        super().__init__(*args, **kwargs)

    # def contribute_to_related_class(self, cls, related):
    #     """
    #     Adds the field to the related class and sets the model instance.

    #     Args:
    #         cls (Model): The model class to which the field is being added.
    #         related (RelatedObject): The related object.
    #     """
    #     super().contribute_to_related_class(cls, related)
    # auto add the vocab to the class
    # setattr(cls, f"{related.get_accessor_name()}_vocab", self.taggable_concepts)


# class TaggableUUIDConcepts(TaggableConcepts):

#     def contribute_to_related_class(self, cls, related):
#         """
#         Adds the field to the related class and sets the model instance.

#         Args:
#             cls (Model): The model class to which the field is being added.
#             related (RelatedObject): The related object.
#         """
#         super().contribute_to_related_class(cls, related)
#         # change object_id field to UUIDField
#         cls._meta.get_field("object_id").__class__ = models.UUIDField()

__all__ = ["ConceptURIField", "ConceptField", "TaggableConcepts"]
