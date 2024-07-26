from django.test import TestCase
from example.vocabularies import SimpleLithology

from research_vocabs.fields import ConceptField


class ConceptFieldTest2(TestCase):
    def setUp(self):
        self.vocabulary = SimpleLithology  # Initialize this with valid data
        self.field = ConceptField(vocabulary=SimpleLithology, max_length=255)

    def test_field_initialization(self):
        self.assertEqual(self.field.vocabulary, self.vocabulary)

    def test_field_choices(self):
        scheme_choices = list(self.vocabulary.choices)
        self.assertEqual(self.field.choices, scheme_choices)

    def test_field_deconstruct(self):
        name, path, args, kwargs = self.field.deconstruct()
        self.assertEqual(kwargs["vocabulary"], self.vocabulary)


# class TaggableConceptsTest(TestCase):
#     def setUp(self):
#         self.manager = TaggableConcepts()

#     def test_keywords_manager_initialization(self):
#         self.assertIsNotNone(self.manager)
