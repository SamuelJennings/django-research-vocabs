import importlib
from pathlib import Path

from rdflib import Graph, URIRef
from rdflib.namespace import RDF, SKOS, NamespaceManager


class VocabFileNotFoundError(Exception):
    """Exception raised when a ConceptScheme subclass cannot find its source file."""

    def __init__(self, class_name, file_path):
        message = f"{class_name} source file {file_path} does not exist"
        super().__init__(message)


class ConceptSchemeMeta(type):
    """Metaclass for ConceptSchemes. This class is responsible for parsing the source file and creating the ConceptScheme class."""

    def __new__(cls, name, bases, attrs, **kwargs):
        if "source" not in attrs or attrs["source"] == "":
            return super().__new__(cls, name, bases, attrs)

        calling_module = importlib.import_module(attrs["__module__"])

        file_path = Path(calling_module.__file__).parent / "vocab_data" / attrs["source"]

        if not file_path.exists():
            raise VocabFileNotFoundError(name, file_path)

        new_class = super().__new__(cls, name, bases, attrs, **kwargs)

        new_class._graph = Graph().parse(file_path, format=attrs.get("format"))

        new_class._nm = NamespaceManager(new_class._graph, bind_namespaces="rdflib")

        new_class._scheme = new_class._graph.value(predicate=RDF.type, object=SKOS.ConceptScheme)
        new_class.URI = str(new_class._scheme)
        new_class._info = new_class.get_concept_meta(new_class._scheme)
        new_class.__doc__ = new_class._info.get("skos:definition", "")
        new_class.SCHEME = new_class.get_concept_label(new_class._scheme)
        return new_class

    @property
    def concepts(cls):
        """Returns a generator of all skos:Concepts in the ConceptScheme"""
        return cls._graph.subjects(predicate=RDF.type, object=SKOS.Concept)

    @property
    def collections(cls):
        """Returns a generator of all skos:Collections in the ConceptScheme"""
        return cls._graph.subjects(predicate=RDF.type, object=SKOS.Collection)

    @property
    def choices(cls):
        """Returns a generator of tuples of (value, label) for all skos:Concepts in the ConceptScheme. This is used to populate Django ChoiceFields in the same way as Django's built-in choices."""
        for concept in cls.concepts:
            yield (str(concept), cls.get_concept_label(concept))

    @property
    def labels(cls):
        """Returns a list of all skos:prefLabels for all skos:Concepts in the ConceptScheme."""
        return [label for _, label in cls.choices]

    @property
    def values(cls):
        """Returns a list of all skos:Concept URIs in the ConceptScheme."""
        return [value for value, _ in cls.choices]

    def get_concept_meta(cls, concept):
        """Returns a dictionary containing metadata associated with a given skos:Concept. Metadata is returned as a dict of predicate: object pairs. Multi-valued predicates are returned as lists."""
        info = {}
        for p, o in cls._graph.predicate_objects(concept):
            if isinstance(o, URIRef):
                o = cls._nm.normalizeUri(o)
            p = cls._nm.normalizeUri(p)

            if p not in info:
                info[str(p)] = str(o)
            else:
                # if the predicate already exists, turn it into a list and append any new values
                if not isinstance(info[p], list):
                    info[p] = [info[p]]
                info[p].append(str(o))

        return info

    def get_concept_label(self, concept, lang="en"):
        """Returns a dictionary of prefLabels for a given subject keyed by language"""

        if isinstance(concept, str):
            concept = URIRef(concept)

        labels = {}
        for obj in self._graph.objects(concept, SKOS.prefLabel):
            labels[obj.language] = obj.value

        try:
            return labels[lang]
        except KeyError:
            return labels[None]
        # return {obj.language: obj.value for obj in self._graph.objects(concept, SKOS.prefLabel)}


class ConceptScheme(metaclass=ConceptSchemeMeta):
    """Base class for all ConceptSchemes. This class should not be used directly with a ConceptField. Instead, use a subclass that points towards a source file.

    Example:

    .. code-block:: python

            from research_vocabs.choices import ConceptScheme

            class SimpleLithology(ConceptScheme):
                source = "simple_lithology.ttl"
    """
