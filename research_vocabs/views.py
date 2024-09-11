from django.http import Http404
from django.views.generic import DetailView, ListView

from .registry import vocab_registry


class VocabularyListView(ListView):
    template_name = "research_vocabs/vocabulary_list.html"
    context_object_name = "vocabularies"

    def get(self, request, *args, **kwargs):
        self.object_list = vocab_registry.items()
        context = self.get_context_data()
        return self.render_to_response(context)


class VocabularyDetailView(DetailView):
    template_name = "research_vocabs/vocabulary_detail.html"

    def get_object(self):
        try:
            self.vocabulary = vocab_registry[self.kwargs["vocabulary"]]
        except KeyError as e:
            msg = "The requested vocabulary could not be found"
            raise Http404(msg) from e
        return self.vocabulary

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vocabulary"] = self.vocabulary

        if "term" in self.kwargs:
            context["concept"] = self.vocabulary.get_concept(self.kwargs["term"])
        else:
            context["is_scheme"] = True
            context["concept"] = self.vocabulary.scheme()
        return context
