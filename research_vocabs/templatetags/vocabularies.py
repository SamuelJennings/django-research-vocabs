from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from rdflib import URIRef

from .. import utils
from ..core import Concept, VocabularyBase

register = template.Library()


@register.simple_tag(takes_context=True)
def i18n_label(context, concept):
    # vocabulary = vocabulary or context.get("vocabulary", None)

    # if isinstance(concept, str):
    #     concept = vocabulary.get_concept(concept)

    request = context.get("request", None)
    lang = getattr(request, "LANGUAGE_CODE", "en")
    return concept.label(lang)


# @register.simple_tag
@register.filter
def label(label):
    """Takes a normalized URI ("SKOS:Concept") and returns the term (e.g. "Concept")"""
    return label.split(":")[-1]


@register.filter
def concept_attr(concept, attr):
    """Returns the value of the specified attribute of the concept."""
    return concept.attrs.get(attr, None)


@register.simple_tag(takes_context=True)
def compute_qname(context, uri, vocabulary: VocabularyBase = None):
    vocabulary = vocabulary or context.get("vocabulary", None)
    uriref = utils.get_URIRef(uri, vocabulary.graph, vocabulary._meta.namespace)
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


def link(value, label):
    return mark_safe(f'<a href="{value}">{label}</a>')


def render_value(value, nm):
    if isinstance(value, Concept):
        return render_to_string("research_vocabs/partials/concept.html", {"value": value})
    elif isinstance(value, URIRef):
        return link(value, nm.normalizeUri(value))
    elif isinstance(value, list):
        li_items = "".join(f"<li>{render_value(v, nm)}</li>" for v in value)
        return mark_safe(f"<ul>{li_items}</ul>")
    else:
        return value


@register.filter
def type_of(obj):
    return type(obj).__name__.lower()


@register.simple_tag
def process_concept(concept, include=None, exclude=None):
    nm = concept.vocabulary.graph.namespace_manager

    if isinstance(include, str):
        include = include.split(",")

    definitions = []

    for k, v in concept.attrs.items():
        value = render_value(v, nm)
        ret = {
            "uri": k,
            "value": v,
            "type": type(v).__name__,
        }
        ret.update(zip(["prefix", "ns", "name"], nm.compute_qname(k)))

        ret["label"] = utils.decamelize(ret["name"])
        definitions.append(ret)
    return definitions


@register.inclusion_tag("research_vocabs/partials/def_list.html")
def render_dl(*args, **kwargs):
    return {"definitions": process_concept(*args, **kwargs)}


@register.inclusion_tag("research_vocabs/partials/table.html")
def render_table(*args, **kwargs):
    return {"definitions": process_concept(*args, **kwargs)}


@register.inclusion_tag("research_vocabs/partials/concept_list.html")
def render_concepts(concepts):
    return {"concept_list": concepts}
