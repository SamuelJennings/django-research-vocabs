from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext as _

from .core import Concept as BaseConcept
from .registry import vocab_registry


class Concept(models.Model):
    """Model for storing skos:Concepts"""

    uri = models.URLField(
        verbose_name=_("URI"),
        unique=True,
    )
    prefLabel = models.CharField(
        verbose_name=_("preferred label"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("concept")
        verbose_name_plural = _("concepts")

    def __str__(self):
        return f"{self.prefLabel}"

    def local_name(self):
        return self.uri.split("/")[-1]

    def namespace(self):
        return self.uri.rsplit("/", 1)[0] + "/"

    def s3(self):
        return f"<{self.uri}>"

    @property
    def vocabulary(self):
        """Get the vocabulary that this concept belongs to from vocab_registry."""
        return vocab_registry.get_vocabulary(self.namespace())

    def as_concept(self):
        return BaseConcept(self.uri, self.vocabulary)


class BaseTaggedConcept(models.Model):
    object_id = models.IntegerField(verbose_name=_("object ID"))
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


class TaggedConcept(BaseTaggedConcept):
    pass


class TaggedUUIDConcept(BaseTaggedConcept):
    object_id = models.UUIDField(verbose_name=_("object ID"))


__all__ = ["Concept", "TaggedConcept", "TaggedUUIDConcept"]
