import importlib
import logging
from pathlib import Path
from urllib.error import HTTPError

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, SKOS, Namespace

from .core import VocabularyBase
from .utils import (
    LocalFilePathError,
    RemoteURLError,
    cache,
    get_translations,
    is_translatable,
)

logger = logging.getLogger(__name__)


class LocalVocabulary(VocabularyBase):
    """Base class for all ConceptSchemes. This class should not be used directly with a ConceptField. Instead, use a subclass that points towards a source file.

    Example:

    .. code-block:: python

            from research_vocabs import LocalVocabulary

            class SimpleLithology(ConceptScheme):
                # locally stored file (path is relative to the class file)
                source = "./vocabs/simple_lithology.ttl"

                # remote file
                source = "https://vocabs.ardc.edu.au/registry/api/resource/downloads/1211/isc2020.ttl"


    """

    def build_graph(self):
        # get file path of class
        calling_module = importlib.import_module(self.__class__.__module__)
        source_kwargs = self._source()

        source_kwargs["source"] = (Path(calling_module.__file__).parent / source_kwargs["source"]).resolve()

        if not source_kwargs["source"].exists():
            raise LocalFilePathError(self.__class__.__name__)

        return Graph().parse(**source_kwargs)


class RemoteVocabulary(LocalVocabulary):
    """A subclass of LocalVocabulary that is specifically for remote sources. The graph is cached for performance.

    Example:

    .. code-block:: python

        from research_vocabs import RemoteVocabulary

        class SimpleLithology(RemoteVocabulary):
            source = "https://vocabs.ardc.edu.au/registry/api/resource/downloads/1211/isc2020.ttl"

    """

    def build_graph(self):
        source_kwargs = self._source()

        # check if graph is in cache
        if graph := cache.get(source_kwargs["source"]):
            return graph
        try:
            graph = Graph().parse(**source_kwargs)
        except HTTPError as e:
            raise RemoteURLError(self.__class__.__name__, source_kwargs["source"]) from e
        else:
            cache.set(source_kwargs["source"], graph, None)
            return graph


class VocabularyBuilder(VocabularyBase):
    """Subclass VocabularyBuilder if you wish to explicitly develop your own concept scheme in Django."""

    def __init__(self, *args, **kwargs):
        self.default_namespace = Namespace("www.example.org/")
        super().__init__()
        # default_ns = self._meta.default_namespace
        # self.default_namespace = Namespace(self.graph.namespaces().get(default_ns))

    def build_graph(self):
        self.graph = Graph()

        self.add_concept(
            self._meta.name,
            SKOS.ConceptScheme,
            self._meta.scheme_attrs,
        )

        self.build_concepts()

        # self.build_collections()
        return self.graph

    def _build_translatable_triples(self, subj, pred, obj):
        self.graph.add((subj, pred, Literal(obj, "en")))
        for lang, msg in get_translations(obj).items():
            self.graph.add((subj, pred, Literal(msg, lang=lang)))

    def build_collections(self):
        collections = self._meta.collections
        ordered_collections = self._meta.ordered_collections
        for name, members in collections.items():
            members = list(self._normalize_members(members))
            if name not in ordered_collections:
                members = sorted(members)

            coll_attrs = {SKOS.member: members}

            rdfType = SKOS.OrderedCollection if name in ordered_collections else SKOS.Collection
            self.add_concept(name, rdfType, coll_attrs)

    def _normalize_members(self, members):
        """Normalize all members to URIRefs."""
        nm = self.graph.namespace_manager
        for member in members:
            if not isinstance(member, URIRef):
                member = nm.expand_curie(member) if ":" in member else self.default_namespace[member]
            yield member

    def build_concepts(self):
        class_attrs = self.__class__.__dict__
        for subj, attrs in class_attrs.items():
            # not the most robust way to distinguish declared concepts
            # but it works for now
            if isinstance(attrs, dict):
                self.add_concept(subj, SKOS.Concept, attrs)

    # @classmethod
    def add_concept(self, term, object: URIRef, attrs: dict):  # noqa: A002
        """
        Adds a type to a subject in the graph and parses a dictionary of attributes.

        Args:
            subj (str): The subject of the triples to be added to the graph. It will be namespaced using the default namespace of the class.
            rdfType (rdflib.term.URIRef): The type to be added to the subject.
            attrs (dict): A dictionary of attributes to be added to the graph. The keys are predicates and the values are objects.

        Returns:
            None

        Example:
            MyVocabulary().add_concept("myVocabTerm", SKOS.Concept, {
                SKOS:prefLabel: "My LocalVocabulary Term",
                SKOS:altLabel: ["My Vocab Term", "MVT"],
                SKOS:definition: "A term in my vocabulary.",
            })
        """
        # make sure subj is properly namespaced
        subject = self.default_namespace[term]

        self.graph.add((subject, RDF.type, object))

        # loop items in meta and add to graph
        for p, o in attrs.items():
            if not isinstance(p, URIRef):
                p = self.graph.namespace_manager.expand_curie(p)

            if isinstance(o, list):
                for entry in o:
                    if is_translatable(entry):
                        self._build_translatable_triples(subject, p, entry)
                    elif isinstance(entry, URIRef):
                        self.graph.add((subject, p, entry))
                    else:
                        self.graph.add((subject, p, Literal(entry)))

            elif is_translatable(o):
                self._build_translatable_triples(subject, p, o)

            else:
                self.graph.add((subject, p, Literal(o)))
