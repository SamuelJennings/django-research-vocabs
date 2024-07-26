from django.test import TestCase

from research_vocabs.registry import vocab_registry


class TestVocabRegistry(TestCase):
    def setUp(self):
        self.vocabs = vocab_registry

    def test_register(self):
        vocab = MockVocabulary()
        self.vocabs.register(vocab)
        self.assertIn("MockVocabulary", self.vocabs.registry)
        self.assertEqual(self.vocabs.get("MockVocabulary"), vocab)

    def test_register_duplicate(self):
        vocab1 = MockVocabulary()
        vocab2 = MockVocabulary()
        self.vocabs.register(vocab1)
        self.vocabs.register(vocab2)
        self.assertIn("MockVocabulary", self.vocabs.registry)
        self.assertEqual(self.vocabs.get("MockVocabulary"), vocab1)

    def test_get(self):
        vocab = MockVocabulary()
        self.vocabs.register(vocab)
        self.assertEqual(self.vocabs.get("MockVocabulary"), vocab)

    def test_get_nonexistent(self):
        with self.assertRaises(KeyError):
            self.vocabs.get("NonexistentVocabulary")


class MockVocabulary:
    pass
