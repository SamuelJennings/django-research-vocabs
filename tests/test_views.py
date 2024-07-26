from django.http import Http404
from django.test import TestCase
from django.urls import reverse

from research_vocabs.registry import vocab_registry
from research_vocabs.views import (
    TermDetailView,
    VocabularyDetailView,
    VocabularyListView,
)


class TestVocabularyListView(TestCase):
    def setUp(self):
        self.vocabs = vocab_registry
        self.url = reverse("vocabularies:list")

    def test_template_name(self):
        view = VocabularyListView()
        self.assertEqual(view.template_name, "research_vocabs/vocabulary_list.html")

    def test_context_object_name(self):
        view = VocabularyListView()
        self.assertEqual(view.context_object_name, "vocabularies")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "research_vocabs/vocabulary_list.html")
        vocabularies = response.context_data["vocabularies"]
        self.assertIn("simplelithology", vocabularies)
        self.assertNotIn("NotRegistered", vocabularies)


class TestVocabularyDetailView(TestCase):
    def setUp(self):
        self.vocabs = vocab_registry

    def test_template_name(self):
        view = VocabularyDetailView()
        self.assertEqual(view.template_name, "research_vocabs/vocabulary_detail.html")


class TestTermDetailView(TestCase):
    def setUp(self):
        self.vocabs = vocab_registry
        self.url = reverse("vocabularies:term", args=["example", "term1"])

    def test_vocab_in_registry(self):
        self.assertIn("example", vocab_registry.registry)

    def test_get_object_existing_term(self):
        view = TermDetailView()
        view.kwargs = {"vocabulary": "example", "term": "term1"}
        obj = view.get_object()
        self.assertEqual(obj, self.term)

    def test_get_object_nonexistent_term(self):
        view = TermDetailView()
        view.kwargs = {"vocabulary": "example", "term": "nonexistent"}
        with self.assertRaises(Http404):
            view.get_object()

    def test_get_object_nonexistent_vocabulary(self):
        view = TermDetailView()
        view.kwargs = {"vocabulary": "nonexistent", "term": "term1"}
        with self.assertRaises(Http404):
            view.get_object()

    def test_template_name(self):
        view = TermDetailView()
        self.assertEqual(view.template_name, "research_vocabs/term_detail.html")

    def test_context_object_name(self):
        view = TermDetailView()
        self.assertEqual(view.context_object_name, "term")
