from django.test import TestCase
from example.choices import SimpleLithology

from research_vocabs.concepts import ConceptScheme, VocabFileNotFoundError


class ConceptSchemeTest(TestCase):
    def setUp(self):
        self.meta = SimpleLithology

    def test_incorrect_source_raises_error(self):
        with self.assertRaises(VocabFileNotFoundError):

            class IncorrectSource(ConceptScheme):
                source = "incorrect_source.ttl"

    def test_concepts_property(self):
        self.assertTrue(hasattr(self.meta, "concepts"))

    def test_collections_property(self):
        self.assertTrue(hasattr(self.meta, "collections"))

    def test_choices_property(self):
        self.assertTrue(hasattr(self.meta, "choices"))

    def test_labels_property(self):
        self.assertTrue(hasattr(self.meta, "labels"))

    def test_values_property(self):
        self.assertTrue(hasattr(self.meta, "values"))

    def test_get_concept_meta_method(self):
        self.assertTrue(hasattr(self.meta, "get_concept_meta"))

    def test_get_concept_label_method(self):
        self.assertTrue(hasattr(self.meta, "get_concept_label"))
