from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from research_vocabs.models import Concept, Vocabulary


class ReadOnlyAdmin(admin.ModelAdmin):
    """
    A read-only admin class that can be used to display information
    without allowing edits.
    """

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Vocabulary)
class VocabularyAdmin(ReadOnlyAdmin):
    list_display = ["name", "label", "linked_uri"]

    def linked_uri(self, obj):
        return mark_safe(f"<a href='{obj.uri}'>{obj.uri}</a>")

    linked_uri.short_description = _("Vocabulary")


@admin.register(Concept)
class ConceptAdmin(ReadOnlyAdmin):
    list_display = ["name", "label", "linked_uri"]
    list_filter = ["vocabulary__label"]

    def linked_uri(self, obj):
        return mark_safe(f"<a href='{obj.uri}'>{obj.vocabulary.label}</a>")  # noqa: S308

    linked_uri.short_description = _("Vocabulary")

    # linked_uri.short_description = _("URI")
