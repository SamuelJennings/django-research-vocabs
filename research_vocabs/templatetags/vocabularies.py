from django import template
from rdflib import URIRef

from .. import utils
from ..core import Concept, VocabularyBase

register = template.Library()


# @register.simple_tag
@register.filter
def label(label):
    """Takes a normalized URI ("SKOS:Concept") and returns the term (e.g. "Concept")"""
    return label.split(":")[-1]


@register.filter
def concept_attr(concept, attr):
    """Returns the value of the specified attribute of the concept."""
    return concept[attr]


@register.simple_tag(takes_context=True)
def compute_qname(context, uri, vocabulary: VocabularyBase = None):
    vocabulary = vocabulary or context.get("vocabulary", None)
    uriref = utils.get_URIRef(uri, vocabulary.graph, vocabulary.default_namespace)
    if vocabulary:
        prefix, ns, name = vocabulary.graph.namespace_manager.compute_qname(uriref)
        return {
            "prefix": prefix,
            "namespace": ns,
            "name": name,
        }


@register.filter
def is_concept(obj):
    return isinstance(obj, Concept)


@register.filter
def is_link(obj):
    return isinstance(obj, URIRef) or isinstance(obj, str) and obj.startswith("http")


@register.filter
def decamelize(text):
    """Converts camel case to snake case."""
    return utils.decamelize(text)


@register.simple_tag(takes_context=True)
def process_attrs(context, concept, exclude=None):
    if exclude is None:
        exclude = []
    elif isinstance(exclude, str):
        exclude = exclude.split(",")
    nm = concept.vocabulary.graph.namespace_manager
    attrs = []
    for k, v in concept.attrs.items():
        prefix, ns, name = nm.compute_qname(k)
        if name in exclude:
            continue
        else:
            predicate = (prefix, ns, name)
        attrs.append((predicate, {"value": v, "is_list": isinstance(v, list)}))
    return attrs
