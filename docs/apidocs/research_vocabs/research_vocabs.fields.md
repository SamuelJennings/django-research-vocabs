# {py:mod}`research_vocabs.fields`

```{py:module} research_vocabs.fields
```

```{autodoc2-docstring} research_vocabs.fields
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`ConceptField <research_vocabs.fields.ConceptField>`
  - ```{autodoc2-docstring} research_vocabs.fields.ConceptField
    :summary:
    ```
* - {py:obj}`TaggableConcepts <research_vocabs.fields.TaggableConcepts>`
  -
````

### API

`````{py:class} ConceptField(scheme, *args, **kwargs)
:canonical: research_vocabs.fields.ConceptField

Bases: {py:obj}`django.db.models.URLField`

```{autodoc2-docstring} research_vocabs.fields.ConceptField
```

```{rubric} Initialization
```

```{autodoc2-docstring} research_vocabs.fields.ConceptField.__init__
```

````{py:method} deconstruct()
:canonical: research_vocabs.fields.ConceptField.deconstruct

````

````{py:method} get_choice_data()
:canonical: research_vocabs.fields.ConceptField.get_choice_data

```{autodoc2-docstring} research_vocabs.fields.ConceptField.get_choice_data
```

````

`````

```{py:class} TaggableConcepts(*args, **kwargs)
:canonical: research_vocabs.fields.TaggableConcepts

Bases: {py:obj}`django.contrib.contenttypes.fields.GenericRelation`

```
