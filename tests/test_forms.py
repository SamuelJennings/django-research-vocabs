from django.core.exceptions import ValidationError
from django.test import TestCase
from example.choices import SimpleLithology

from research_vocabs.forms import KeywordChoiceField, KeywordMultiChoiceField


class KeywordChoiceFieldTest(TestCase):
    def setUp(self):
        self.scheme = SimpleLithology
        self.valid_uri = next(self.scheme.choices)[0]
        self.field = KeywordChoiceField(scheme=self.scheme)

    def test_field_initialization(self):
        self.assertEqual(self.field.scheme, self.scheme)

    def test_field_choices(self):
        self.assertEqual(self.field.choices, list(self.scheme.choices))

    def test_clean_method(self):
        # Assuming the scheme has a validate method
        with self.assertRaises(ValidationError):
            self.field.clean("invalid_uri")

    def test_clean_method_with_value(self):
        cleaned_value = self.field.clean(self.valid_uri)
        self.assertEqual(cleaned_value, [self.valid_uri])


class KeywordMultiChoiceFieldTest(KeywordChoiceFieldTest):
    def setup(self):
        super().setUp()
        self.field = KeywordMultiChoiceField(scheme=self.scheme)

    def test_clean_method_with_value(self):
        cleaned_value = self.field.clean(self.valid_uri)
        self.assertEqual(cleaned_value, [self.valid_uri])
