from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from research_vocabs.models import Concept

from .forms import AdminForm
from .models import Lithology, TestModel

admin.site.register(Lithology)


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    form = AdminForm


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ["name", "label", "vocab_name", "linked_uri"]

    def linked_uri(self, obj):
        return mark_safe(f"<a href='{obj.uri}'>{obj.uri}</a>")  # noqa: S308

    linked_uri.short_description = _("URI")
