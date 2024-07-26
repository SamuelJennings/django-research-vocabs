from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ResearchVocabConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "research_vocabs"
    verbose_name = _("LocalVocabulary")
    verbose_name_plural = _("Vocabularies")
