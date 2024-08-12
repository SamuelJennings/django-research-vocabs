import logging

from django.urls import reverse_lazy
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, SKOS

from .options import VocabMeta
from .utils import get_translations, get_URIRef, is_translatable

logger = logging.getLogger(__name__)

# TODO:
# - grouped choices (e.g. by collection or tree structure)
# - include or exclude concepts using list of values (can use a filter method, can use collections)


class ConceptAttrs(dict):
    def __init__(self, graph, namespace, **kwargs):
        self.graph = graph
        self.namespace = namespace
        super().__init__(**kwargs)

    def __getitem__(self, key):
        key = get_URIRef(key, self.graph, self.namespace)
        return super().__getitem__(key)

    def get(self, key, default=None):
        key = get_URIRef(key, self.graph, self.namespace)
        return super().get(key, default)


class Concept:
    """A class representing a SKOS Concept in a given RDF graph. This class is used to extract metadata from a Concept and provide a more user-friendly interface for accessing metadata."""

    rdf_type = SKOS.Concept
    definition_types = [
        "skos:definition",
        "dcterms:description",
        # "purl:definition",
    ]

    def __init__(self, URI: str | URIRef, vocabulary=None, rdf_type=None):
        """Initializes a new Concept instance.

        Args:
            URI (str, URIRef): The URI of the Concept. If a string is provided, it must either be a URI or a CURIE (compact representation - e.g. "materials:Wood"). It will be converted to a URIRef object using the graph's namespace manager.
            graph (Graph): The RDF graph containing the Concept.
        """
        if rdf_type:
            self.rdf_type = rdf_type
        self.vocabulary = vocabulary
        self.namespace = self.vocabulary.ns
        self.graph = vocabulary.graph
        self.nm = self.graph.namespace_manager
        self.URI = get_URIRef(URI, self.graph, self.namespace)
        pre, ns, name = self.nm.compute_qname(self.URI)
        self.name = name
        self._attrs = ConceptAttrs(self.graph, self.namespace)
        if (self.URI, RDF.type, None) not in self.graph:
            msg = f"'{self.name}' not found in {self.vocabulary.scheme().name}."
            raise ValueError(msg)

    def __str__(self):
        return self.name
        # return self.nm.normalizeUri(self.URI)

    def __html__(self):
        curie = self.nm.normalizeUri(self.URI)
        return f'<a href="{self.get_absolute_url()}">{curie}</a>'

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

    def definition(self):
        """Returns the definition of the Concept."""
        for pred in self.definition_types:
            if pred := self.attrs.get(pred):
                return pred

        return ""

    # def label(self, lang=settings.LANGUAGE_CODE):
    def label(self, lang="en"):
        labels = {}
        for obj in self.graph.objects(self.URI, SKOS.prefLabel):
            labels[obj.language] = obj.value
        return labels.get(lang, labels.get(None, ""))

    def get_absolute_url(self):
        return reverse_lazy(
            "vocabularies:term", kwargs={"vocabulary": self.vocabulary.scheme().name, "term": self.name}
        )


class VocabularyBase(metaclass=VocabMeta):
    """
    Base class for vocabulary instances.
    """

    graph: Graph | None = None
    _scheme: Concept | None = None
    _concepts: list[Concept] | None = None
    _choices: list[tuple[str, str]] | None = None

    def __init__(self, include_only: list = None):
        self.ns = Namespace(self._meta.namespace)
        if self.graph is None:
            # assigns graph directly to class so that it is shared across all instances
            self.__class__.graph = self.build_graph()

        self.graph.bind(self._meta.prefix, self.ns)
        self.namespaces = dict(self.graph.namespaces())
        self.build_collections()
        self.include_only = include_only

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

    def label(self, lang="en"):
        return self.scheme().label(lang)

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
        """Returns a python list of tuples of (value, label) for all skos:Concepts in the ConceptScheme. This is used to populate Django ChoiceFields in the same way as Django's built-in choices."""
        if self._choices:
            return self._choices

        if self.include_only:
            # only return those concepts specified in the "include" list
            self._choices = [self.get_choice_tuple(self.get_concept(i)) for i in self.include_only]
            return self._choices

        if coll := self._meta.from_collection:
            # if "from_collection" is specified as a Meta option, return only the members of that collection

            collection = Concept(coll, self, rdf_type=SKOS.Collection)

            self._choices = [self.get_choice_tuple(member) for member in collection["skos:member"]]
            return self._choices

        self._choices = [self.get_choice_tuple(concept) for concept in self.concepts()]
        return self._choices

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
        return tree

    def get_absolute_url(self):
        name = self.scheme().name
        return reverse_lazy("vocabularies:detail", kwargs={"vocabulary": name})

    def get_choice_tuple(self, concept: Concept):
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
        """Returns a generator of all subjects where the RDF.type is a SKOS.Concept."""
        if self.__class__._concepts:
            return self.__class__._concepts

        self.__class__._concepts = [
            Concept(s, self) for s in self.graph.subjects(predicate=RDF.type, object=SKOS.Concept)
        ]
        if self._meta.ordered:
            self.__class__._concepts = sorted(self.__class__._concepts, key=lambda x: x.label())
        return self.__class__._concepts

    def get_concept(self, name: str | URIRef) -> Concept:
        """Returns a Concept object from the Graph based on the name or URI."""
        return Concept(name, self)

    # BUILDER METHODS

    def build_collections(self):
        collections = self._meta.collections
        ordered_collections = self._meta.ordered_collections
        for name, collection in collections.items():
            collection["skos:member"] = [get_URIRef(m, self.graph, self.ns) for m in collection["skos:member"]]

            if not collection.ordered:
                collection["skos:member"] = sorted(collection["skos:member"])

            rdfType = SKOS.OrderedCollection if name in ordered_collections else SKOS.Collection
            self.add_concept(name, rdfType, collection)

    def _build_translatable_triples(self, subj, pred, obj):
        self.graph.add((subj, pred, Literal(obj, "en")))
        for lang, msg in get_translations(obj).items():
            self.graph.add((subj, pred, Literal(msg, lang=lang)))

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
        subject = self.ns[term]

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
