from django.core.exceptions import ValidationError
from django.test import TestCase
from example.choices import SimpleLithology

from research_vocabs.fields import ConceptField, TaggableConcepts


class ConceptFieldTest(TestCase):
    def setUp(self):
        self.scheme = SimpleLithology  # Initialize this with valid data
        self.field = ConceptField(scheme=self.scheme)

    def test_field_initialization(self):
        self.assertEqual(self.field.scheme, self.scheme)

    def test_field_choices(self):
        scheme_choices = list(self.scheme.choices)
        self.assertEqual(self.field.choices, scheme_choices)

    def test_field_deconstruct(self):
        name, path, args, kwargs = self.field.deconstruct()
        self.assertEqual(kwargs["scheme"], self.scheme)


class TaggableConceptsTest(TestCase):
    def setUp(self):
        self.manager = TaggableConcepts()

    def test_keywords_manager_initialization(self):
        self.assertIsNotNone(self.manager)
