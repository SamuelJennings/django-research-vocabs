from django.db import models
from django.utils.translation import gettext_lazy as _

from research_vocabs.fields import ConceptField, TaggableConcepts

from .choices import SimpleLithology


class TestModel(models.Model):
    name = models.CharField(max_length=100)

    concept = ConceptField(scheme=SimpleLithology, null=True, blank=True)

    tagged_concepts = TaggableConcepts()
