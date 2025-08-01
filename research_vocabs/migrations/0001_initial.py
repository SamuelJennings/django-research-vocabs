# Generated by Django 5.2.3 on 2025-06-11 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vocabulary",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True, verbose_name="name")),
                ("label", models.CharField(max_length=255, verbose_name="preferred label")),
                ("description", models.TextField(blank=True, null=True, verbose_name="description")),
                ("uri", models.URLField(unique=True, verbose_name="URI")),
                (
                    "meta",
                    models.JSONField(
                        blank=True,
                        help_text="Additional metadata about the vocabulary",
                        null=True,
                        verbose_name="metadata",
                    ),
                ),
            ],
            options={
                "verbose_name": "vocabulary",
                "verbose_name_plural": "vocabularies",
            },
        ),
        migrations.CreateModel(
            name="Concept",
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
                (
                    "vocabulary",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="concepts",
                        to="research_vocabs.vocabulary",
                        verbose_name="vocabulary",
                    ),
                ),
            ],
            options={
                "verbose_name": "concept",
                "verbose_name_plural": "concepts",
            },
        ),
    ]
