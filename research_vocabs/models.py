from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models, transaction
from django.utils.translation import gettext as _

from .registry import vocab_registry


class Vocabulary(models.Model):
    """Model for storing vocabularies used in the application."""

    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        unique=True,
    )
    label = models.CharField(
        verbose_name=_("preferred label"),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
        null=True,
    )
    uri = models.URLField(
        verbose_name=_("URI"),
        unique=True,
    )
    meta = models.JSONField(
        verbose_name=_("metadata"),
        blank=True,
        null=True,
        help_text=_("Additional metadata about the vocabulary"),
    )

    class Meta:
        verbose_name = _("vocabulary")
        verbose_name_plural = _("vocabularies")

    def __str__(self):
        return self.name


class ConceptManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class AbstractConcept(models.Model):
    """Model for storing skos:Concepts"""

    objects = ConceptManager()

    _vocabulary = None

    # vocab_name = models.CharField(
    #     verbose_name=_("vocabulary"),
    #     max_length=255,
    # )
    uri = models.URLField(
        verbose_name=_("URI"),
        unique=True,
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
    )
    label = models.CharField(
        verbose_name=_("preferred label"),
        max_length=255,
    )
    meta = models.JSONField(
        verbose_name=_("metadata"),
        blank=True,
        null=True,
        help_text=_("Additional metadata about the concept, such as synonyms, definitions, etc."),
    )

    class Meta:
        abstract = True
        verbose_name = _("concept")
        verbose_name_plural = _("concepts")

    def __str__(self):
        return f"{self.vocabulary}: {self.name}"

    def __repr__(self):
        return f"<{self}>"

    # @property
    # def vocabulary(self):
    #     """Get the vocabulary that the concept belongs to from vocab_registry."""
    #     return vocab_registry[self.vocabulary]

    # def as_concept(self):
    #     return self.vocabulary.get_concept(self.name)

    @classmethod
    def add_concept(cls, concept):
        defaults = cls._get_defaults(concept)
        # vocabulary_name may be set to None on purpose by subclasses wishing to store values from a single vocabulary

        # if cls.vocab_name is not None:
        # defaults["vocab_name"] = concept.vocabulary.scheme().name

        return cls.objects.update_or_create(uri=concept.URI, defaults=defaults)

    @classmethod
    def _get_defaults(cls, concept):
        return {
            "name": concept.name,
            "label": concept.label(),
            "meta": concept.attrs,
        }

    @classmethod
    def preload(cls):
        """If a vocabulary is set, preload all concepts from the vocabulary. The alternative is to slowly populate the table as concepts are added via form fields, etc."""
        if cls._vocabulary is not None:
            # raise ValueError("No vocabulary set for this concept model.")
            with transaction.atomic():
                for concept in cls._vocabulary.concepts():
                    cls.add_concept(concept)


class Concept(AbstractConcept):
    vocabulary = models.ForeignKey(
        Vocabulary,
        verbose_name=_("vocabulary"),
        on_delete=models.CASCADE,
        related_name="concepts",
    )

    class Meta:
        verbose_name = _("concept")
        verbose_name_plural = _("concepts")
        unique_together = ("vocabulary", "name")

    @classmethod
    def preload(cls):
        """If a vocabulary is set, preload all concepts from the vocabulary. The alternative is to slowly populate the table as concepts are added via form fields, etc."""
        with transaction.atomic():
            for name, vocab in vocab_registry.items():
                vocabulary, created = Vocabulary.objects.update_or_create(
                    name=name,
                    defaults={
                        "label": vocab.scheme().label(),
                        "uri": vocab.scheme().URI,
                        # "meta": vocab.scheme().attrs,
                    },
                )
                for concept in vocab.concepts():
                    cls.objects.update_or_create(
                        vocabulary=vocabulary,
                        name=concept.name,
                        defaults={
                            "uri": concept.URI,
                            "label": concept.label(),
                            # "meta": concept.attrs,
                        },
                    )
                    # cls.add_concept(concept)
                concept_count = len(vocab.concepts())
                print(f"Preloaded {concept_count} concepts for vocabulary: {name}")

    @classmethod
    def get_for_vocabulary(cls, vocabulary):
        """Get all concepts for a given vocabulary. vocabulary can be a Vocabulary instance, a string (name of the vocabulary), or a registered vocabulary object."""
        if isinstance(vocabulary, str):
            return cls.objects.filter(vocabulary__name=vocabulary)

        vocab_name = vocabulary().scheme().name if hasattr(vocabulary, "scheme") else vocabulary.name
        return cls.objects.filter(vocabulary__name=vocab_name)


class BaseTaggedConcept(models.Model):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(
        "contenttypes.ContentType",
        verbose_name=_("content type"),
        on_delete=models.CASCADE,
    )
    content_object = GenericForeignKey("content_type", "object_id")
    concept = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

    class Meta:
        abstract = True
        verbose_name = _("tagged concept")
        verbose_name_plural = _("tagged concepts")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __init__(self, *args, **kwargs):
        URI = kwargs.pop("URI", None)
        scheme = kwargs.pop("scheme", None)
        super().__init__(*args, **kwargs)
        if URI and scheme:
            self.concept, _ = self.concept_model.add_concept(URI, scheme)

    def save(self, *args, **kwargs):
        if not self.pk and not self.concept.pk:
            self.concept.save()
        return super().save(*args, **kwargs)

    @property
    def concept_model(cls):
        return cls._meta.get_field("concept").related_model
