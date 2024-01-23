#!/usr/bin/env python

"""
test_django-research-vocabs
------------

Tests for `django-research-vocabs` models module.
"""

from django.test import TestCase
from model_bakery import baker

from research_vocabs.fields import TaggableConcepts


class KeywordsManagerTest(TestCase):
    def setUp(self):
        self.manager = TaggableConcepts()

    def test_keywords_manager_initialization(self):
        self.assertIsNotNone(self.manager)

    def test_keywords_manager_through_property(self):
        self.assertEqual(self.manager.through, "keywords.KeywordThrough")
