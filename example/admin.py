from django.contrib import admin

from research_vocabs.admin import ConceptAdmin, VocabularyAdmin
from research_vocabs.models import Concept, Vocabulary

from .forms import AdminForm
from .models import Lithology, TestModel

admin.site.register(Lithology)
admin.site.register(Vocabulary, VocabularyAdmin)
admin.site.register(Concept, ConceptAdmin)


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    form = AdminForm
