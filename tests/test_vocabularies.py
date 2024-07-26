from django.test import TestCase
from example.vocabularies import CustomMaterials
from rdflib.namespace import SKOS

from research_vocabs.utils import LocalFilePathError
from research_vocabs.vocabularies import LocalVocabulary


class TestLocalVocabulary(TestCase):
    def test_local_source(self):
        class LocalSource(LocalVocabulary):
            class Meta:
                source = "./example/vocab_data/simple_lithology.ttl"

        vocab = LocalSource()
        self.assertIsInstance(vocab, LocalVocabulary)
        self.assertEqual(vocab.scheme().name, "simplelithology")

    def test_incorrect_local_source_raises_error(self):
        with self.assertRaises(LocalFilePathError):

            class IncorrectSource(LocalVocabulary):
                class Meta:
                    source = "incorrect_source.ttl"

            IncorrectSource()

    # def test_remote_source(self):
    #     class RemoteSource(LocalVocabulary):
    #         class Meta:
    #             source = "https://vocabs.ardc.edu.au/registry/api/resource/downloads/214/ga_simple-lithology_v0-1.ttl"

    #     vocab = RemoteSource()
    #     self.assertIsInstance(vocab, LocalVocabulary)
    #     self.assertEqual(vocab.scheme().name, "simplelithology")

    # def test_incorrect_remote_source_raises_error(self):
    #     with self.assertRaises(RemoteURLError):

    #         class IncorrectSource(LocalVocabulary):
    #             class Meta:
    #                 source = "https://google.com/incorrect_source.ttl"

    #         IncorrectSource()

    def test_source_parse_kwargs(self):
        class LocalSource(LocalVocabulary):
            class Meta:
                source = {
                    "source": "./example/vocab_data/simple_lithology.ttl",
                    "format": "turtle",
                }

        self.assertIsInstance(LocalSource(), LocalVocabulary)

    def test_incorrect_source_type(self):
        with self.assertRaises(TypeError):

            class IncorrectSource(LocalVocabulary):
                class Meta:
                    source = 123

            IncorrectSource()


class TestVocabularyBuilder(TestCase):
    def setUp(self):
        self.vocabulary = CustomMaterials()

    def test_add_concept(self):
        self.vocabulary.add_concept("test", SKOS.Concept, {"skos:prefLabel": "test"})
        concept = self.vocabulary.get_concept("mats:test")
        self.assertTrue(concept.name, "test")

    def test_build_concepts(self):
        self.vocabulary.build_concepts()
        self.assertEqual(len(self.vocabulary.concepts()), 2)

    def test_build_collections(self):
        self.vocabulary.build_collections()
        collectionA = self.vocabulary.get_concept("mats:collectionA")
        self.assertEqual(collectionA.name, "collectionA")
        members = collectionA["skos:member"]
        self.assertEqual(len(members), 2)

    def test_normalize_collection_members(self):
        members = ["Wood", "skos:prefLabel"]
        normalized = list(self.vocabulary._normalize_members(members))
        expected1 = self.vocabulary.default_namespace["Wood"]
        expected2 = SKOS.prefLabel
        self.assertEqual(normalized[0], expected1)
        self.assertEqual(normalized[1], expected2)

    def test_build_translatable_triples(self):
        pass
