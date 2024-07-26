from django.test import TestCase
from django.utils.translation import gettext_lazy
from rdflib import Graph, URIRef

from research_vocabs import utils


class TestUtils(TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_get_URIRef_with_uri_string(self):
        uri_string = "http://example.com/resource"
        result = utils.get_URIRef(uri_string, self.graph)
        expected = URIRef(uri_string)
        self.assertEqual(result, expected)

    def test_get_URIRef_with_curie(self):
        curie = "skos:Concept"
        self.graph.namespace_manager.bind("skos", "http://www.w3.org/2004/02/skos/core#")
        result = utils.get_URIRef(curie, self.graph)
        expected = URIRef("http://www.w3.org/2004/02/skos/core#Concept")
        self.assertEqual(result, expected)

    def test_get_URIRef_with_uriref_object(self):
        uriref = URIRef("http://example.com/resource")
        result = utils.get_URIRef(uriref, self.graph)
        expected = uriref
        self.assertEqual(result, expected)

    def test_get_setting(self):
        from django.conf import settings

        settings.VOCABULARY_DEFAULT_PREFIX = "TEST"
        result = utils.get_setting("DEFAULT_PREFIX")
        self.assertEqual(result, "TEST")

    def test_is_translatable(self):
        msg = gettext_lazy("Hello")
        self.assertTrue(utils.is_translatable(msg))
        self.assertFalse(utils.is_translatable("Hello"))

    def test_LocalFilePathError(self):
        klass = "ConceptScheme"
        with self.assertRaises(utils.LocalFilePathError) as cm:
            raise utils.LocalFilePathError(klass)
        self.assertEqual(str(cm.exception), f"{klass} - no source file exists at the specified location")

    def test_RemoteURLError(self):
        class_name = "ConceptScheme"
        url = "http://example.com/source"
        with self.assertRaises(utils.RemoteURLError) as cm:
            raise utils.RemoteURLError(class_name, url)
        expected_message = f"{class_name} remote source URL <{url}> is not valid"
        self.assertEqual(str(cm.exception), expected_message)

    def test_get_translations(self):
        msg = gettext_lazy("hello")
        translations = utils.get_translations(msg)
        print(translations)
        # expected_translations = {"en": "hello", "fr": "bonjour", "es": "hola"}
        # self.assertEqual(translations, expected_translations)

    def test_decamelize(self):
        value = "helloWorld"
        result = utils.decamelize(value)
        expected = "hello world"
        self.assertEqual(result, expected)
