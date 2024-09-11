import logging

logger = logging.getLogger(__name__)


class VocabularyOptions:
    name = ""
    """The name of the vocabulary. This is used to internally identify the vocabulary for things like URL routing."""

    prefix = ""
    """The prefix for the vocabulary. This is used to namespace all concepts in the vocabulary."""

    namespace = ""
    """The root namespace for the vocabulary. This is used to namespace all concepts in the vocabulary. It should be a valid URI."""

    ordered = True
    """Whether the concepts in the vocabulary should be ordered by label in select boxes. Set this to False to maintain the order specified in the graph."""

    from_collection = ""
    """The name of a SKOS:Collection used to restrict accepted values to a subset of concepts within the graph."""

    rdf_type = "skos:Concept"
    """The RDF type used to identify terms in the vocabulary. This is used to filter concepts in the graph."""

    scheme_attrs = {}
    collections = {}
    ordered_collections = []
    source: str | dict = ""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k.startswith("_"):
                continue
            elif getattr(self, k, None) is None:
                msg = f"Invalid Meta option: {k}"
                raise AttributeError(msg)
            else:
                setattr(self, k, v)


class VocabMeta(type):
    def __new__(cls, name, bases, attrs):
        meta_class = attrs.pop("Meta", None)

        if meta_class:
            attrs["_meta"] = VocabularyOptions(**meta_class.__dict__)

        return super().__new__(cls, name, bases, attrs)
