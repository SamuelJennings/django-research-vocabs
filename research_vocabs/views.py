from django.http import Http404
from django.views.generic import DetailView, ListView

from .registry import vocab_registry


class VocabularyListView(ListView):
    template_name = "research_vocabs/vocabulary_list.html"
    context_object_name = "vocabularies"

    def get(self, request, *args, **kwargs):
        self.object_list = vocab_registry.registry
        context = self.get_context_data()
        return self.render_to_response(context)


class VocabularyDetailView(DetailView):
    template_name = "research_vocabs/vocabulary_detail.html"

    def get_object(self):
        try:
            self.vocabulary = vocab_registry.registry[self.kwargs["vocabulary"]]
        except KeyError as e:
            msg = f"LocalVocabulary {self.kwargs['vocabulary']} not found"
            raise Http404(msg) from e
        else:
            return self.vocabulary

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vocabulary"] = self.vocabulary

        history = self.vocabulary.scheme()["skos:changeNote"]
        if not isinstance(history, list) and history is not None:
            history = [history]
        context["history"] = history

        return context


class TermDetailView(VocabularyDetailView):
    template_name = "research_vocabs/term_detail.html"
    context_object_name = "concept"
    description_exclude = ["type", "definition", "prefLabel"]

    def get_object(self):
        self.vocabulary = super().get_object()
        try:
            return self.vocabulary.get_concept("lith:" + self.kwargs["term"])
        except ValueError as e:
            msg = f"Term {self.kwargs['term']} not found in {self.kwargs['vocabulary']}"
            raise Http404(msg) from e
