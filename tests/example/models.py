from django.db import models

from research_vocabs.fields import ConceptField, TaggableConcepts

from .vocabularies import FeatureType, SamplingFeatureGeoType


class TestModel(models.Model):
    name = models.CharField(max_length=100)

    concept_label = ConceptField(
        vocabulary=SamplingFeatureGeoType, include_only=["point", "polygon"], max_length=255, null=True, blank=True
    )

    concept_builder = ConceptField(verbose_name="Status", vocabulary=FeatureType, max_length=255, null=True, blank=True)

    tagged_concepts = TaggableConcepts()
