from django.db.models import Manager
from django.db.models.fields.related_descriptors import create_forward_many_to_many_manager


class RelatedConceptManager(Manager):
    def __init__(self, instance, vocab_name=None):
        super().__init__()
        self.instance = instance
        self.vocab_name = vocab_name

    def get_queryset(self):
        return super().get_queryset().filter(vocabulary__name=self.vocab_name)


class ManyToManyConceptDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        manager = create_forward_many_to_many_manager(instance._meta.get_field(self.field.name).rel, instance.__class__)

        base_manager = manager(instance)
        key = self.field.custom_key
        return base_manager.filter(**{key[0]: key[1]})
