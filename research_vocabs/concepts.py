from .bases import LocalStorageBase, RemoteStorageBase, SchemeBuilderBase


class LocalConceptScheme(metaclass=LocalStorageBase):
    """Base class for all ConceptSchemes. This class should not be used directly with a ConceptField. Instead, use a subclass that points towards a source file.

    Example:

    .. code-block:: python

            from research_vocabs.choices import ConceptScheme

            class SimpleLithology(ConceptScheme):
                source = "simple_lithology.ttl"
    """

    pass


class RemoteConceptScheme(metaclass=RemoteStorageBase):
    """A base class for creating a concept scheme from a remote source. This class should not be used directly with a ConceptField. Instead, use a subclass that points towards a source file."""

    pass


class ConceptSchemeBuilder(metaclass=SchemeBuilderBase):
    """Subclass `ConceptSchemeBuilder if you wish to explicitly develop your own concept scheme in Django."""

    pass
