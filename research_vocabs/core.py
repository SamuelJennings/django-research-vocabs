import logging

from django.urls import reverse, reverse_lazy
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, SKOS

from .utils import get_URIRef

logger = logging.getLogger(__name__)

# TODO:
# - grouped choices (e.g. by collection or tree structure)
# - include or exclude concepts using list of values (can use a filter method, can use collections)


class Concept:
    """A class representing a SKOS Concept in a given RDF graph. This class is used to extract metadata from a Concept and provide a more user-friendly interface for accessing metadata."""

    rdf_type = SKOS.Concept

    def __init__(self, URI: str | URIRef, vocabulary=None, rdf_type=None):
        """Initializes a new Concept instance.

        Args:
            URI (str, URIRef): The URI of the Concept. If a string is provided, it must either be a URI or a CURIE (compact representation - e.g. "materials:Wood"). It will be converted to a URIRef object using the graph's namespace manager.
            graph (Graph): The RDF graph containing the Concept.
        """
        if rdf_type:
            self.rdf_type = rdf_type
        self.vocabulary = vocabulary
        self.def_ns = self.vocabulary.default_namespace
        self.graph = vocabulary.graph
        self.nm = self.graph.namespace_manager

        self.URI = get_URIRef(URI, self.graph, self.def_ns)
        pre, ns, name = self.nm.compute_qname(self.URI)
        self.prefix = pre
        self.name = name
        self.namespace = ns
        self._attrs = {}
        if (self.URI, RDF.type, None) not in self.graph:
            msg = f"'{self.name}' not found in {self.vocabulary.scheme().name}."
            raise ValueError(msg)

    def __getitem__(self, key):
        key = get_URIRef(key, self.graph)
        return self.attrs.get(key, None)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Concept: {self.name}>"

    def __len__(self):
        return len(self.name)

    @property
    def attrs(self):
        """Returns a dictionary containing metadata associated with a given skos:Concept. Metadata is returned as a dict of predicate: object pairs. Multi-valued predicates are returned as lists."""

        if self._attrs:
            return self._attrs

        for p, o in self.graph.predicate_objects(self.URI):
            # if isinstance(o, URIRef):
            #     o = self.nm.normalizeUri(o)
            # p = self.nm.normalizeUri(p)

            # if the object is a URI, convert it to a Concept object
            if (o, RDF.type, SKOS.Concept) in self.graph:
                o = Concept(o, self.vocabulary)

            if p not in self._attrs:
                self._attrs[p] = o
            else:
                # if the predicate already exists, turn it into a list and append any new values
                if not isinstance(self._attrs[p], list):
                    self._attrs[p] = [self._attrs[p]]
                self._attrs[p].append(o)

        return self._attrs

    # def label(self, lang=settings.LANGUAGE_CODE):
    def label(self, lang="en"):
        # lang = lang.lower().split("-")[0]
        labels = {}
        for obj in self.graph.objects(self.URI, SKOS.prefLabel):
            labels[obj.language] = obj.value
        # probably should default to settings.LANGUAGE_CODE
        return labels.get(lang, labels.get(None, ""))

    def get_absolute_url(self):
        return reverse_lazy(
            "vocabularies:term", kwargs={"vocabulary": self.vocabulary.scheme().name, "term": self.name}
        )


class VocabularyOptions:
    name = None
    """The name of the vocabulary."""

    prefix = ""
    namespaces = {}
    default_namespace = ""
    scheme_attrs = {}
    collections = {}
    ordered_collections = []
    name = ""
    source: str | dict = ""
    store_uris = False
    term_identifier = SKOS.Concept

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


class VocabularyBase(metaclass=VocabMeta):
    """
    Base class for vocabulary instances.
    """

    graph: Graph | None = None
    _scheme: Concept | None = None

    def __init__(self, include: str | URIRef | list = "", exclude: str | URIRef | list = "", tree=False, group=True):
        if self.graph is None:
            # assigns graph directly to class so that it is shared across all instances
            self.__class__.graph = self.build_graph()

        self.bind_namespaces()

    def __str__(self):
        return self.scheme().label("en")

    def __iter__(self):
        return self.choices

    def _source(self):
        """Source is always parsed into a dict for consistency."""
        if isinstance(self._meta.source, str):
            return {"source": self._meta.source}
        elif isinstance(self._meta.source, dict):
            return self._meta.source
        else:
            msg = (
                f"source must be a string or a dictionary. You provided {type(self._meta.source)}: {self._meta.source}"
            )
            raise TypeError(msg)

    @property
    def labels(self):
        """Returns a list of all skos:prefLabels for all skos:Concepts in the ConceptScheme."""
        return [label for _, label in self.choices]

    @property
    def values(self):
        """Returns a list of all skos:Concept URIs in the ConceptScheme."""
        return [value for value, _ in self.choices]

    @property
    def choices(self):
        """Returns a generator of tuples of (value, label) for all skos:Concepts in the ConceptScheme. This is used to populate Django ChoiceFields in the same way as Django's built-in choices."""
        for concept in self.concepts():
            yield self.get_choice_tuple(concept)

    def tree(self):
        """Returns a tree structure of the vocabulary."""
        # { "id" : "name", "parent" : "#" or SKOS.Broader, "text" : "label" },

        def get_parents(concept):
            broader = concept.attrs.get(SKOS.broader)
            if isinstance(broader, Concept):
                return broader.name
            else:
                return "#"

        tree = []
        for concept in self.concepts():
            parents = concept.attrs.get(SKOS.broader)
            if isinstance(parents, list):
                for parent in parents:
                    tree.append(
                        {
                            "id": concept.name,
                            "parent": parent.name,
                            "text": concept.label(),
                            "a_attr": {"href": concept.get_absolute_url()},
                        }
                    )
            elif isinstance(parents, Concept):
                tree.append(
                    {
                        "id": concept.name,
                        "parent": parents.name,
                        "text": concept.label(),
                        "a_attr": {"href": concept.get_absolute_url()},
                    }
                )
            else:
                tree.append(
                    {
                        "id": concept.name,
                        "parent": "#",
                        "text": concept.label(),
                        "a_attr": {"href": concept.get_absolute_url()},
                    }
                )
        print(tree[0])
        return tree

    def get_absolute_url(self):
        name = self.scheme().name
        return reverse_lazy("vocabularies:detail", kwargs={"vocabulary": name})

    def bind_namespaces(self):
        for prefix, uri in self._meta.namespaces.items():
            if not uri:
                uri = reverse("vocabularies:detail", kwargs={"vocabulary": self._meta.name})

            self.graph.bind(prefix, Namespace(uri))
        # extract the default namespace from the graph
        self.namespaces = dict(self.graph.namespaces())
        self.default_uri = self.namespaces.get(self._meta.default_namespace, "http://example.org/")
        self.default_namespace = Namespace(self.default_uri)

    def get_choice_tuple(self, concept: Concept):
        if self._meta.store_uris:
            return str(concept), concept.label()
        else:
            return concept.name, concept.label()

    def build_graph(self):
        """This should be overriden in the subclass to build the graph from a local file or remote URL."""
        raise NotImplementedError("You must implement the build_graph method in your subclass.")

    def scheme(self) -> Concept:
        if not self._scheme:
            scheme = self.graph.value(predicate=RDF.type, object=SKOS.ConceptScheme)
            self._scheme = Concept(scheme, self, rdf_type=SKOS.ConceptScheme)
        return self._scheme

    def concepts(self):
        """Returns a generator of all subjects where the RDF.type is a klass.term_identifier."""
        concepts = [
            Concept(s, self) for s in self.graph.subjects(predicate=RDF.type, object=self._meta.term_identifier)
        ]
        return concepts

    def get_concept(self, name: str | URIRef) -> Concept:
        """Returns a Concept object from the Graph based on the name or URI."""
        return Concept(name, self)
