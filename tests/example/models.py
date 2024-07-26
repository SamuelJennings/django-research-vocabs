from django.db import models

from research_vocabs.fields import ConceptField, TaggableConcepts

from .vocabularies import SimpleLithology


class TestModel(models.Model):
    name = models.CharField(max_length=100)

    concept_label = ConceptField(vocabulary=SimpleLithology, max_length=255, null=True, blank=True)

    tagged_concepts = TaggableConcepts()
