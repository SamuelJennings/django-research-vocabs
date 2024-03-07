from django.conf import settings
from django.utils import translation
from django.utils.translation import trans_real
from rdflib import namespace as ns


class LocalFilePathError(Exception):
    """Exception raised when a ConceptScheme subclass cannot find its source file."""

    def __init__(self, class_name, file_path):
        message = f"{class_name} source file {file_path} does not exist"
        super().__init__(message)


class RemoteURLValidationError(Exception):
    """Exception raised when a ConceptScheme subclass cannot find its source file."""

    def __init__(self, class_name, url):
        message = f"{class_name} remote source URL <{url}> is not valid"
        super().__init__(message)


class NamespaceError(Exception):
    """Exception raised when a ConceptScheme subclass cannot find its source file."""

    def __init__(self, value):
        message = (
            f"Meta.namespace must be either a `str` or a `rdflib.Namespace` object. You provided{type(value)}: {value}"
        )
        super().__init__(message)


def get_default_namespace():
    """Get the default namespace for the project."""
    return getattr(settings, "VOCABULARY_NAMESPACE", "https://example.com/vocabularies/")


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


def is_known_namespace(input_str):
    """Takes an input_str as "namespace.term" and returns True if the namespace is importable from rdflib.namespace."""
    if not isinstance(input_str, str):
        raise TypeError(f"input_str must be a string. You provided {type(input_str)}: {input_str}")

    namespace_str = input_str.split(".")[0]

    # try import namespace from rdflib.namespaces
    try:
        # Get the attribute dynamically
        return getattr(ns, namespace_str.upper())
    except AttributeError:
        return False

    # Get the term from the namespace
    return True
