from django.db import models

from research_vocabs.fields import ConceptField, ConceptManyToManyField
from research_vocabs.models import AbstractConcept, Concept

from .vocabularies import CustomMaterials, FeatureType, SimpleLithology


class Lithology(AbstractConcept):
    """Users can define their own model to store a specific vocabulary and link to it from other models."""

    vocabulary_name = None
    vocabulary = None
    _vocabulary = SimpleLithology()

    class Meta:
        verbose_name = "Lithology"
        verbose_name_plural = "Lithologies"


class TestModel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    concept_label = ConceptField(
        vocabulary=SimpleLithology,
        max_length=255,
        null=True,
        blank=True,
    )

    concept_builder = ConceptField(
        verbose_name="Status",
        vocabulary=FeatureType,
        max_length=255,
        null=True,
        blank=True,
    )

    # m2m = models.ManyToManyField(
    #     Lithology,
    #     related_name="test_objects",
    #     blank=True,
    #     verbose_name="Lithologies",
    # )

    materials = ConceptManyToManyField(
        vocabulary=CustomMaterials,
        blank=True,
        verbose_name="materials",
    )

    test = ConceptManyToManyField(
        vocabulary=SimpleLithology,
        verbose_name="basic geographical test",
        default="unspecified",
    )

    taggable_concepts = models.ManyToManyField(
        Concept, related_name="test_objects", blank=True, verbose_name="Taggable Concepts"
    )

    def __str__(self):
        return f"{self.name}"


# class LithologyTree(MP_Node, Concept):
