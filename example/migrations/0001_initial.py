# Generated by Django 5.2.3 on 2025-06-11 11:26

import example.vocabularies
import research_vocabs.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("research_vocabs", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lithology",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uri", models.URLField(unique=True, verbose_name="URI")),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                ("label", models.CharField(max_length=255, verbose_name="preferred label")),
                (
                    "meta",
                    models.JSONField(
                        blank=True,
                        help_text="Additional metadata about the concept, such as synonyms, definitions, etc.",
                        null=True,
                        verbose_name="metadata",
                    ),
                ),
            ],
            options={
                "verbose_name": "Lithology",
                "verbose_name_plural": "Lithologies",
            },
        ),
        migrations.CreateModel(
            name="TestModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "concept_label",
                    research_vocabs.fields.ConceptField(
                        blank=True,
                        max_length=47,
                        null=True,
                        verbose_name="Simple Lithology",
                        vocabulary=example.vocabularies.SimpleLithology,
                    ),
                ),
                (
                    "concept_builder",
                    research_vocabs.fields.ConceptField(
                        blank=True,
                        max_length=28,
                        null=True,
                        verbose_name="Status",
                        vocabulary=example.vocabularies.FeatureType,
                    ),
                ),
                (
                    "taggable_concepts",
                    models.ManyToManyField(
                        blank=True,
                        related_name="test_objects",
                        to="research_vocabs.concept",
                        verbose_name="Taggable Concepts",
                    ),
                ),
                (
                    "test",
                    research_vocabs.fields.ConceptManyToManyField(
                        default="unspecified",
                        to="research_vocabs.concept",
                        verbose_name="basic geographical test",
                        vocabulary=example.vocabularies.SimpleLithology,
                    ),
                ),
            ],
        ),
    ]
