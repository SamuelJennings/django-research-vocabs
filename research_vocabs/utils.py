import re

from django.conf import settings
from django.core.cache import caches
from django.utils import translation
from django.utils.safestring import SafeString
from django.utils.translation import trans_real
from rdflib import Graph, URIRef


class LocalFilePathError(Exception):
    """Exception raised when a ConceptScheme subclass cannot find its source file."""

    def __init__(self, klass):
        message = f"{klass} - no source file exists at the specified location"
        super().__init__(message)


class RemoteURLError(Exception):
    """Exception raised when a ConceptScheme subclass cannot find its source file."""

    def __init__(self, class_name, url):
        message = f"{class_name} remote source URL <{url}> is not valid"
        super().__init__(message)


def is_translatable(msg):
    """Check if a string is wrapped in a translatable function. Not sure how comprehensive this is."""
    return hasattr(msg, "_proxy____cast")


def get_translations(msg):
    """
    Function to get all available translations of a translatable string.
    """
    og_msg = str(msg)
    translations = {}
    for lang in trans_real.get_languages():
        with translation.override(lang):
            if translated := trans_real.catalog()._catalog.get(og_msg):
                translations[lang] = translated
    return translations


def get_setting(key):
    local_setting = {
        "DEFAULT_PREFIX": "DEFAULT",
        "DEFAULT_CACHE": "vocabularies",
    }
    return getattr(settings, f"VOCABULARY_{key}", local_setting[key])


def get_URIRef(val: str | URIRef, graph: Graph, ns):
    """
    Normalizes val to a URIRef object.

    Args:
        val (str | URIRef): The value to be normalized. It can be a URI string, a valid CURIE (e.g. "SKOS:Concept"), or a URIRef object.
        graph (Graph): The graph object used for expanding CURIEs.

    Returns:
        URIRef: A URIRef object.

    """
    # calling .strip() on a SafeString will convert to regular python str
    if isinstance(val, SafeString):
        val = val.strip()

    if isinstance(val, URIRef):
        return val
    elif val.startswith("http"):
        return URIRef(val)
    elif ":" in val:
        return graph.namespace_manager.expand_curie(val)
    else:
        return ns[val]


cache = caches[get_setting("DEFAULT_CACHE")]


VOCABULARY_CACHE = {
    "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
    "LOCATION": settings.BASE_DIR / ".vocabularies-cache",
}


def decamelize(value):
    """De-camelizes a camel case string."""
    return " ".join(re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)", value)).lower()
