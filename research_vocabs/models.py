from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.encoding import force_str
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
from taggit.models import GenericTaggedItemBase


class Concept(models.Model):
    """Model for storing keywords data"""

    label = models.CharField(verbose_name=pgettext_lazy("Preferred label of concept", "label"), max_length=255)

    URI = models.URLField(_("URI"), max_length=200, null=True, blank=True)

    slug = models.SlugField(
        verbose_name=pgettext_lazy("A concept URL slug", "slug"),
        max_length=255,
        allow_unicode=True,
        blank=True,
        null=True,
    )

    scheme_label = models.CharField(
        verbose_name=pgettext_lazy("Label of concept scheme", "scheme"),
        max_length=255,
        blank=True,
        null=True,
    )
    scheme_URI = models.URLField(
        verbose_name=pgettext_lazy("URI of concept scheme", "scheme URI"),
        blank=True,
        null=True,
    )
    scheme_slug = models.SlugField(
        verbose_name=pgettext_lazy("A concept scheme URL slug", "scheme slug"),
        max_length=255,
        allow_unicode=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("keyword")
        verbose_name_plural = _("keywords")
        default_related_name = "keywords"
        unique_together = ["label", "scheme_URI"]

    def __str__(self):
        return force_str(self.label)

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            self.slug = slugify(self.label)
            self.scheme_slug = slugify(self.scheme_label)
        else:
            return super().save(*args, **kwargs)

    @classmethod
    def add_concept(cls, URI, scheme):
        """Accepts a URI and a ConceptScheme object and adds the concept to the data. If the concept already exists, it will be returned, otherwise a new keyword will be created."""

        return cls.objects.get_or_create(
            URI=URI,
            defaults={
                "label": scheme.get_concept_label(URI),
                "scheme_label": scheme.SCHEME,
                "scheme_URI": scheme.URI,
            },
        )


class TaggedConcept(models.Model):
    object_id = models.IntegerField(verbose_name=_("object ID"), db_index=True)
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
        verbose_name = _("tagged concept")
        verbose_name_plural = _("tagged concepts")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    @property
    def concept_model(cls):
        return cls._meta.get_field("concept").related_model

    @classmethod
    def create(cls, content_object, URI, scheme):
        """Accepts a URI and a ConceptScheme object and adds the concept to the data. If the concept already exists, it will be returned, otherwise a new keyword will be created."""

        concept, created = cls.concept_model.add_concept(URI, scheme)
        if created:
            concept.save()

        return cls(content_object=content_object, concept=concept)


# class KeywordThrough(GenericTaggedItemBase):
#     tag = models.ForeignKey(
#         Concept,
#         on_delete=models.CASCADE,
#         related_name="%(app_label)s_%(class)s_items",
#     )

#     class Meta:
#         verbose_name = _("keyword")
#         verbose_name_plural = _("keywords")
#         app_label = "research_vocabs"
