from django.contrib import admin

# import render_to_string
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from research_vocabs.models import Concept

from .models import TestModel

admin.site.register(TestModel, admin.ModelAdmin)

# render_to_string("base.html", {"foo": "bar"})
mark_safe


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = [
        "label",
        "URI_display",
        "scheme_display",
        "tag_count",
    ]
    list_filter = [
        "scheme_label",
    ]

    def URI_display(self, obj):
        return mark_safe(f"<a href='{obj.URI}'>{obj.URI}</a>")

    URI_display.short_description = "Label"

    def scheme_display(self, obj):
        return mark_safe(f"<a href='{obj.scheme_URI}'>{obj.scheme_label}</a>")

    scheme_display.short_description = "Scheme"

    def tag_count(self, obj):
        return obj.research_vocabs_taggedconcept_items.count()
