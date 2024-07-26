#!/usr/bin/env python

"""
test_django-research-vocabs
------------

Tests for `django-research-vocabs` models module.
"""

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from example.models import TestModel
from example.vocabularies import SimpleLithology

from research_vocabs.models import Concept, TaggedConcept


class ConceptModelTest(TestCase):
    def setUp(self):
        self.concept = Concept.objects.create(
            label="Test Label",
            URI="http://example.com/concept",
            scheme_label="Test Scheme",
            scheme_URI="http://example.com",
        )

    def test_concept_creation(self):
        self.assertEqual(self.concept.label, "Test Label")
        self.assertEqual(self.concept.URI, "http://example.com/concept")
        self.assertEqual(self.concept.scheme_label, "Test Scheme")
        self.assertEqual(self.concept.scheme_URI, "http://example.com")

    def test_string_representation(self):
        self.assertEqual(str(self.concept), self.concept.label)


class TaggedConceptModelTest(TestCase):
    def setUp(self):
        self.scheme = SimpleLithology
        self.choices = list(self.scheme.choices)
        self.concept = Concept.objects.create(
            label="Test Label",
            URI="http://example.com/concept",
            scheme_label="Test Scheme",
            scheme_URI="http://example.com",
        )
        self.tagged_concept = TaggedConcept.objects.create(
            object_id=1, content_type=ContentType.objects.get_for_model(Concept), concept=self.concept
        )

    def test_tagged_concept_creation(self):
        self.assertEqual(self.tagged_concept.object_id, 1)
        self.assertEqual(self.tagged_concept.content_type, ContentType.objects.get_for_model(Concept))
        self.assertEqual(self.tagged_concept.concept, self.concept)

    def test_save_with_URI_and_scheme(self):
        URI = self.choices[1][0]
        label = self.choices[1][1]
        tagged_concept = TaggedConcept(URI=URI, scheme=self.scheme)

        self.assertEqual(tagged_concept.concept.URI, URI)
        self.assertEqual(tagged_concept.concept.label, label)
        self.assertEqual(tagged_concept.concept.scheme_label, self.scheme.SCHEME)
        self.assertEqual(tagged_concept.concept.scheme_URI, self.scheme.URI)


class TestModelTest(TestCase):
    def setUp(self):
        self.scheme = SimpleLithology
        self.choices = list(self.scheme.choices)
        self.URI = self.choices[1][0]
        self.label = self.choices[1][1]
        self.model = TestModel.objects.create(
            name="Test Name",
            concept=self.URI,
        )

    def test_model_creation(self):
        self.assertEqual(self.model.name, "Test Name")
        self.assertEqual(self.model.concept, self.URI)

    def test_tagged_concepts_add(self):
        tagged_concept = TaggedConcept(URI=self.URI, scheme=self.scheme)
        self.model.tagged_concepts.add(tagged_concept, bulk=False)
        self.assertEqual(self.model.tagged_concepts.count(), 1)
