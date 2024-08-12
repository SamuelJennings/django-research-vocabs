from django.urls import path

from .views import VocabularyDetailView, VocabularyListView

app_name = "vocabularies"
urlpatterns = [
    path("", VocabularyListView.as_view(), name="list"),
    path("<vocabulary>/", VocabularyDetailView.as_view(), name="detail"),
    path("<vocabulary>/<term>/", VocabularyDetailView.as_view(), name="term"),
]
