from django.test import TestCase
from example.vocabularies import ISC2020, SimpleLithology
from rdflib import URIRef

from research_vocabs.core import Concept, VocabMeta, VocabularyBase


class TestConcept(TestCase):
    def setUp(self):
        self.vocabulary = SimpleLithology()
        self.graph = self.vocabulary.graph
        self.concept = Concept("lith:granite", self.vocabulary)

    def test_initialize_concept(self):
        self.assertIsInstance(self.concept, Concept)
        self.assertEqual(self.concept.URI, URIRef("http://resource.geosciml.org/classifier/cgi/lithology/granite"))
        # self.assertEqual(self.concept.prefix, "lith")
        self.assertEqual(self.concept.name, "granite")
        self.assertEqual(self.concept.namespace, URIRef("http://resource.geosciml.org/classifier/cgi/lithology/"))

    def test_incorrect_initialize_concept(self):
        with self.assertRaises(ValueError):
            Concept("lith:nonexistant", self.vocabulary)

    def test_str(self):
        self.assertEqual(str(self.concept), "http://resource.geosciml.org/classifier/cgi/lithology/granite")

    def test_concept_label(self):
        label = self.concept.label()
        self.assertNotEqual(label, "")
        self.assertIsInstance(label, str)
        self.assertEqual(label, "granite")

    def test_concept_label_with_lang(self):
        label = self.concept.label("es")
        self.assertEqual(label, "granito")

    def test_concept_label_missing_lang(self):
        # test with a language that doesn't exist in the vocabulary
        label = self.concept.label("pt")
        self.assertEqual(label, "granite")

    def test_concept_label_lang_fallback(self):
        # test with a sub-language code (e.g. en-us)
        # should fallback to the base language (e.g. en)
        label = self.concept.label("en-us")
        self.assertEqual(label, "granite")

    def test_attrs(self):
        self.assertIsInstance(self.concept.attrs, dict)
        self.assertNotEqual(self.concept.attrs, {})
        self.assertIn(URIRef("http://www.w3.org/2004/02/skos/core#prefLabel"), self.concept.attrs)

    def test_getitem(self):
        granitoid = URIRef("http://resource.geosciml.org/classifier/cgi/lithology/granitoid")
        self.assertEqual(self.concept["skos:broader"], granitoid)

    def test_getitem_multivalue(self):
        # multi-value items are returned as lists
        labels = self.concept["skos:prefLabel"]
        self.assertIsInstance(labels, list)
        self.assertEqual(len(labels), 17)
        self.assertIn("granite", [str(l) for l in labels])


class TestVocabularyBase(TestCase):
    def setUp(self):
        self.vocabulary = SimpleLithology()

    def test_initialize_vocabulary(self):
        self.assertIsInstance(self.vocabulary, VocabularyBase)
        # self.assertEqual(self.vocabulary._meta.source, "./vocab_data/simple_lithology.ttl")
        self.assertIsNotNone(self.vocabulary.graph)
        # self.assertEqual(self.vocabulary.term_identifier, SKOS.Concept)
        # self.assertIsNone(self.vocabulary._scheme)
        # self.assertFalse(self.vocabulary.store_uris)

    def test_str(self):
        self.assertEqual(str(self.vocabulary), "Simple Lithology")

    def test_iter(self):
        choices = list(self.vocabulary)
        self.assertIsInstance(choices, list)
        self.assertEqual(len(choices), 265)

    def test_labels(self):
        labels = self.vocabulary.labels
        self.assertIsInstance(labels, list)
        self.assertEqual(len(labels), 265)
        self.assertIn("mudstone", labels)
        self.assertNotIn("clastic_mudstone", labels)

    def test_values(self):
        values = self.vocabulary.values
        self.assertIsInstance(values, list)
        self.assertEqual(len(values), 265)
        self.assertIn("clastic_mudstone", values)
        self.assertNotIn("mudstone", values)

    def test_choices(self):
        choices = list(self.vocabulary.choices)
        self.assertIsInstance(choices, list)
        self.assertEqual(len(choices), 265)
        self.assertIn(("clastic_mudstone", "mudstone"), choices)

    def test_get_choice_tuple(self):
        concept = Concept("lith:clastic_mudstone", self.vocabulary)
        choice_tuple = self.vocabulary.get_choice_tuple(concept)
        self.assertIsInstance(choice_tuple, tuple)
        self.assertEqual(choice_tuple, ("clastic_mudstone", "mudstone"))

    def test_subclass_implements_build_graph(self):
        class TestVocabulary(VocabularyBase):
            class Meta:
                source = "your_source"

        with self.assertRaises(NotImplementedError):
            TestVocabulary()
            # self.vocabulary.build_graph()

    def test_scheme(self):
        scheme = self.vocabulary.scheme()
        self.assertIsInstance(scheme, Concept)
        self.assertEqual(
            scheme.URI, URIRef("http://resource.geosciml.org/classifierscheme/cgi/2016.01/simplelithology")
        )

    def test_concepts(self):
        concepts = list(self.vocabulary.concepts())
        self.assertIsInstance(concepts, list)
        self.assertEqual(len(concepts), 265)
        self.assertIsInstance(concepts[0], Concept)
        self.assertEqual(
            concepts[0].URI, URIRef("http://resource.geosciml.org/classifier/cgi/lithology/acidic_igneous_material")
        )
        self.assertEqual(
            concepts[1].URI, URIRef("http://resource.geosciml.org/classifier/cgi/lithology/alkali-olivine_basalt")
        )

    def test_get_concept(self):
        concept = self.vocabulary.get_concept("lith:alkali-olivine_basalt")
        self.assertIsInstance(concept, Concept)
        self.assertEqual(
            concept.URI, URIRef("http://resource.geosciml.org/classifier/cgi/lithology/alkali-olivine_basalt")
        )

    def test_get_absolute_url(self):
        url = self.vocabulary.get_absolute_url()
        self.assertEqual(url, "/vocabularies/simplelithology/")


class TestMetaClass(TestCase):
    def setUp(self):
        self.vocabulary = ISC2020

    def test_valid_option(self):
        meta = VocabMeta(source="your_source")
        self.assertEqual(meta.source, "your_source")

    def test_invalid_option(self):
        with self.assertRaises(AttributeError):
            VocabMeta(unknown_option="invalid")

    def test_private_option(self):
        meta = VocabMeta(_private_option="invalid")
        self.assertNotIn("_private_option", meta.__dict__)

    def test_rdf_type_option(self):
        class TestVocab(ISC2020):
            class Meta:
                rdf_type = "gts:GeochronologicBoundary"

        vocabulary = TestVocab()

        self.assertEqual(TestVocab._meta.rdf_type, "skos:Concept")

    # def test_nordf_type_option(self):
    #     class TestVocab(ISC2020):
    #         class Meta:
    #             rdf_type = "skos:Concept"

    #     self.assertEqual(TestVocab._meta.rdf_type, "skos:Concept")
