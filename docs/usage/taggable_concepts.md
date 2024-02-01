# Generic Tagging

## TaggableConcepts Field

The `TaggableConcepts` field is a custom field that extends the `GenericRelation` class in Django and establishes a generic relation to the `research_vocabs.models.TaggedConcept` model. This allows the model that has this field to have a set of tagged concepts associated with it.

To use it, first import the `TaggableConcepts` field from the `research_vocabs.fields`. Then, add the TaggableConcepts field to your model like so:

```python
from research_vocabs.fields import TaggableConcepts

class MyModel(models.Model):
    # Other fields here...
    concepts = TaggableConcepts()

```

## Associating concepts with a model instance

```python
from research_vocabs.models import TaggedConcept, Concept
from myapp.models import MyModel

# Create a new instance of MyModel
instance = MyModel.objects.create()

# get an existing or create a new Concept
concept = Concept.objects.get_or_create(
    URI='http://www.w3.org/2004/02/skos/core#Concept',
    scheme=MyConceptScheme
)

# Create a new TaggedConcept
tagged_concept = TaggedConcept(concept=concept)

# Associate the TaggedConcept with the MyModel instance
instance.concepts.add(tagged_concept)

# Save the MyModel instance
instance.save()
```
