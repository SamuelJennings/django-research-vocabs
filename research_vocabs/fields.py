from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import URLField


class MissingConceptSchemeError(Exception):
    """Raised when a concept scheme is not passed as an argument to the ConceptField class."""

    msg = "ConceptField requires a ConceptScheme object to be passed as an argument."

    # def __init__(self):
    # super().__init__("ConceptField requires a ConceptScheme object to be passed as an argument.")


class ConceptField(URLField):
    """
    A custom field class that extends the URLField class. This class is used to represent a concept field
    in a concept scheme. The concept scheme is passed as an argument during the initialization of the class.

    Attributes:
        scheme (ConceptScheme): The concept scheme that this field belongs to.

    Methods:

        get_choice_data(): Returns the concept metadata from the scheme using the DB value.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the ConceptField with the given scheme. The scheme's choices are also set as the choices for this field.

        Args:
            scheme (ConceptScheme): The concept scheme that this field belongs to.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.scheme = kwargs.pop("scheme", None)
        if not self.scheme:
            raise MissingConceptSchemeError
        kwargs["choices"] = self.scheme.choices
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        """Used to recreate the field."""
        name, path, args, kwargs = super().deconstruct()
        kwargs["scheme"] = self.scheme
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
        kwargs["to"] = "research_vocabs.TaggedConcept"
        super().__init__(*args, **kwargs)
