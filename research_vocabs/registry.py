class VocabRegistry(dict):
    """A registry of vocabularies that have been used in the application."""

    def __init__(self):
        self.registry = {}

    def items(self):
        return self.registry.items()

    def register(self, vocab):
        name = vocab.scheme().name
        if name not in self.registry:
            self.registry[name] = vocab

    def get(self, name):
        return self.registry[name]


vocab_registry = VocabRegistry()
