# Usage

Before you can use either the `ConceptField` or `TaggableConcepts` fields, you must first download and save your research vocabulary as a supported file format. `django-research-vocabs` uses `rdflib` under the hood to parse your vocabulary file. Therefore, you must save your vocabulary as one of the file formats supported by `rdflib`. Some common formats include:

- [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/)
- [N-Triples](https://www.w3.org/TR/n-triples/)
- [N-Quads](https://www.w3.org/TR/n-quads/)
- [Turtle](https://www.w3.org/TR/turtle/)
- [JSON-LD](https://www.w3.org/TR/json-ld/)


```{attention}
`django-research-vocabs` does not support remote calls to online vocabularies. Instead, you must download and save the vocabulary file locally in your Django project. This allows you to use the vocabulary even if the remote server is down or the vocabulary is no longer available online. It also guards against changes to the vocabulary that may break your application.
```

## 1. Save to local directory

Download and save your research vocabulary as a supported RDF file in your app directory. For example,

```directory
your_project/
    your_app/
        vocabularies/
            my_concept_scheme.rdf
        apps.py
        ...
```

## 2. Define your new ConceptScheme

Create a new `ConceptScheme` subclass and direct it to the appropriate source file:

```python

# in your_app/choices.py or any other suitable location 
# that makes sense to you

from research_vocabs.concepts import ConceptScheme

class MyConceptScheme(ConceptScheme):

    # relative path to your vocabulary file
    source = 'vocabularies/my_concept_scheme.rdf'

```

## 3. Decide how you want to use your vocabulary

`django-reserach-vocabs` provides two ways to use your vocabulary: `ConceptField` and `TaggableConcepts`. 

`ConceptField`: subclasses `URLField` and adds the scheme concepts as the default choices argument.

`TaggableConcepts`: a `GenericRelation` that allows you to associate any model instance with any number of concepts.


```{toctree}
:caption: Fields
:maxdepth: 1
:hidden:

concept_field
taggable_concepts

```
