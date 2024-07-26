from django.test import TestCase
from django.urls import reverse

from research_vocabs.views import (
    TermDetailView,
    VocabularyDetailView,
    VocabularyListView,
)


class TestURLs(TestCase):
    def test_vocabularies_list_url(self):
        url = reverse("vocabularies:list")
        self.assertEqual(url, "/vocabularies/")

    def test_vocabulary_url(self):
        vocabulary = "example"
        url = reverse("vocabularies:detail", args=[vocabulary])
        self.assertEqual(url, f"/vocabularies/{vocabulary}/")

    def test_term_url(self):
        vocabulary = "example"
        term = "term1"
        url = reverse("vocabularies:term", args=[vocabulary, term])
        self.assertEqual(url, f"/vocabularies/{vocabulary}/{term}/")

    def test_vocabularies_list_view(self):
        # view = VocabularyListView.as_view()
        response = self.client.get(reverse("vocabularies:list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.view_class, VocabularyListView)

    def test_vocabulary_view(self):
        vocabulary = "example"
        response = self.client.get(reverse("vocabularies:detail", args=[vocabulary]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.view_class, VocabularyDetailView)

    def test_term_view(self):
        vocabulary = "example"
        term = "term1"
        response = self.client.get(reverse("vocabularies:term", args=[vocabulary, term]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.view_class, TermDetailView)
