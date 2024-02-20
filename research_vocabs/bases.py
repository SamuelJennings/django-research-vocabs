import importlib
import logging
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rdflib import Graph, Literal, URIRef
from rdflib import namespace as ns
from rdflib.namespace import RDF, SKOS, Namespace, NamespaceManager

from .utils import (
    LocalFilePathError,
    RemoteURLValidationError,
    get_translations,
    is_translatable,
)

logger = logging.getLogger(__name__)


class ConceptSchemaBase(type):

    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [b for b in bases if isinstance(b, ConceptSchemaBase)]
        if not parents:
            return super().__new__(cls, name, bases, attrs, **kwargs)

        meta_cls = attrs.pop("Meta", None)
        if meta_cls:
            meta_dict = {}
            for attr_name, attr_value in vars(meta_cls).items():
                # Store meta attributes in the class namespace
                meta_dict[attr_name] = attr_value

            # attrs["_meta"] = meta_dict
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)
        new_class._meta = meta_dict

        if not hasattr(new_class, "_graph"):
            new_class._build_graph(name, attrs)

        new_class._nm = NamespaceManager(new_class._graph, bind_namespaces="rdflib")

        new_class._scheme = new_class._graph.value(predicate=RDF.type, object=SKOS.ConceptScheme)
        new_class.URI = str(new_class._scheme)
        new_class._info = new_class.get_concept_meta(new_class._scheme)
        new_class.name = new_class.get_concept_label(new_class.URI)
        new_class.__doc__ = new_class._info.get("skos:definition", "")
        new_class.SCHEME = new_class.get_concept_label(new_class._scheme)

        return new_class

    def _build_graph(cls, name, attrs):
        return Graph()

    def concepts(cls, graph=None):
        """Returns a generator of all skos:Concepts in the ConceptScheme"""
        graph = graph or cls._graph
        return graph.subjects(predicate=RDF.type, object=SKOS.Concept)

    @property
    def nm(cls):
        return cls._graph.namespace_manager

    @property
    def collections(cls):
        """Returns a generator of all skos:Collections in the ConceptScheme"""
        return cls._graph.subjects(predicate=RDF.type, object=SKOS.Collection)

    @property
    def choices(cls):
        """Returns a generator of tuples of (value, label) for all skos:Concepts in the ConceptScheme. This is used to populate Django ChoiceFields in the same way as Django's built-in choices."""
        for concept in cls.concepts():
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
                o = cls.nm.normalizeUri(o)
            p = cls.nm.normalizeUri(p)

            if p not in info:
                info[str(p)] = str(o)
            else:
                # if the predicate already exists, turn it into a list and append any new values
                if not isinstance(info[p], list):
                    info[p] = [info[p]]
                info[p].append(str(o))

        return info

    def get_concept_label(cls, concept, lang="en"):
        """Returns a dictionary of prefLabels for a given subject keyed by language"""

        if isinstance(concept, str):
            concept = URIRef(concept)

        labels = {}
        for obj in cls._graph.objects(concept, SKOS.prefLabel):
            labels[obj.language] = obj.value

        # print(labels)
        try:
            return labels[lang]
        except KeyError:
            # "BLANK"
            return labels.get(None, "BLANK")

    def get_URI_from_label(cls, label):
        """Returns the URI of a concept given its label."""
        for subj in cls.concepts():
            if cls.get_concept_label(subj) == label:
                return subj


class LocalStorageBase(ConceptSchemaBase):
    """A metaclass that allows vocabularies to be loaded from a local file. This is useful for testing and development."""

    def _build_graph(cls, name, attrs):
        calling_module = importlib.import_module(attrs["__module__"])
        file_path = Path(calling_module.__file__).parent / "vocab_data" / cls._meta.get("source", "")

        if not file_path.exists():
            raise LocalFilePathError(name, file_path)

        cls._graph = Graph().parse(file_path, format=cls._meta.get("format"))


class RemoteStorageBase(ConceptSchemaBase):
    """A metaclass that allows vocabularies to be loaded from a remote file. This is useful for production use."""

    def _build_graph(cls, name, attrs):
        source = cls._meta.get("source", "")
        try:
            URLValidator()(attrs["source"])
        except ValidationError as err:
            raise RemoteURLValidationError(name, source) from err

        cls._graph = Graph().parse(source)


class SchemeBuilderBase(ConceptSchemaBase):

    def _build_graph(cls, name, attrs):

        # create a new graph
        cls._graph = Graph()

        cls.default_namespace = Namespace(cls._meta.get("namespace", "http://example.com/"))

        cls.parse_rdfType("", SKOS.ConceptScheme, cls._meta["conceptscheme"])

        cls.parse_concepts(attrs)

        # parse collections
        cls.parse_collections(SKOS.Collection, cls._meta.get("collections"))
        cls.parse_collections(SKOS.OrderedCollection, cls._meta.get("ordered_collections"))

    def _build_translatable_triples(cls, subj, pred, obj):
        cls._graph.add((subj, pred, Literal(obj, "en")))
        for lang, msg in get_translations(obj).items():
            cls._graph.add((subj, pred, Literal(msg, lang=lang)))

    def parse_collections(cls, collType, collections):
        if collections is None:
            return
        for coll, members in collections.items():
            coll_attrs = {SKOS.member: [cls.default_namespace[m] for m in members]}
            cls.parse_rdfType(cls.default_namespace[coll], collType, coll_attrs)

    def parse_concepts(cls, concepts):
        for subj, attrs in concepts.items():
            # skip private attributes
            if subj.startswith("_"):
                continue
            cls.parse_rdfType(subj, SKOS.Concept, attrs)

    def parse_rdfType(cls, subj, rdfType: URIRef, attrs: dict):
        """
        This class method adds a type to a subject in the graph and parses a dictionary of attributes.

        Args:
            subj (str): The subject of the triples to be added to the graph. It will be namespaced using the default namespace of the class.
            rdfType (rdflib.term.URIRef): The type to be added to the subject.
            attrs (dict): A dictionary of attributes to be added to the graph. The keys are predicates and the values are objects.

        Returns:
            None

        Example:
            subj = "example_subject"
            rdfType = rdflib.term.URIRef("http://example.org/type")
            attrs = {
                rdflib.term.URIRef("http://example.org/predicate1"): rdflib.term.Literal("object1"),
                rdflib.term.URIRef("http://example.org/predicate2"): [rdflib.term.Literal("object2"), rdflib.term.Literal("object3")]
            }
            MyClass.parse_rdfType(subj, rdfType, attrs)
        """
        # make sure subj is properly namespaced
        subj = cls.default_namespace[subj]

        cls._graph.add((subj, RDF.type, rdfType))

        cls.parse_attr_dict(subj, attrs)

    def parse_attr_dict(cls, subj, attrs):
        """
        This class method parses a dictionary of attributes and adds them to a graph as triples.

        Args:
            subj (rdflib.term.URIRef): The subject of the triples to be added to the graph.
            attrs (dict): A dictionary of attributes to be added to the graph. The keys are predicates and the values are objects. Predicates may be rdflib.term.URIRef or strings that can be imported from namespaces in the base rdflib package.

        Returns:
            None

        Example:
            attrs = {
                SKOS.prefLabel: _("Wood"),
                SKOS.altLabel: [_("Timber"), _("Lumber")],
                "SKOS.definition": _(
                    "A hard fibrous material that forms the main substance of the trunk or branches of a tree or shrub."
                ),
            }
            subj = rdflib.term.URIRef("http://example.org/subject")
            MyClass.parse_attr_dict(subj, attrs)
        """
        # loop items in meta and add to graph
        for pred, obj in attrs.items():

            pred = cls.parse_attr_predicate(pred)

            if isinstance(obj, list):
                for literal in obj:
                    if is_translatable(literal):
                        cls._build_translatable_triples(subj, pred, literal)
                    else:
                        cls._graph.add((subj, pred, Literal(literal)))

            elif is_translatable(obj):
                cls._build_translatable_triples(subj, pred, obj)

            else:
                cls._graph.add((subj, pred, Literal(obj)))

    def parse_attr_predicate(cls, pred):
        """Handles predicates specified in the attr dict. If the predicate is not a URIRef, we will check if it exists in the base rdflib namespace and import it. We then return the predicate as a URIRef and add the namespace to the graph's namespace manager."""
        if isinstance(pred, str):
            if len(pred.split(".")) > 2:
                return pred
            namespace_str, term = pred.split(".")
            # try import namespace from rdflib.namespaces
            try:
                # Get the attribute dynamically
                namespace = getattr(ns, namespace_str)
            except AttributeError as e:
                # reraise with a custom message
                raise AttributeError(  # noqa: TRY003
                    f"The attribute '{namespace_str}' specified in {cls.__module__}.{cls.__name__} does not exist in the 'ns' module."
                ) from e

            # Get the term from the namespace
            pred = getattr(namespace, term)
            # Add the namespace to the graph's namespace manager if it does not already exist
            if namespace_str not in cls.nm:
                logging.debug(f"Binding namespace {namespace_str} to {namespace}")
                cls.nm.bind(namespace_str, namespace)

        return pred
