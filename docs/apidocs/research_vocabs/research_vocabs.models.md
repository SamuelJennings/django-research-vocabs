# {py:mod}`research_vocabs.models`

```{py:module} research_vocabs.models
```

```{autodoc2-docstring} research_vocabs.models
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Concept <research_vocabs.models.Concept>`
  - ```{autodoc2-docstring} research_vocabs.models.Concept
    :summary:
    ```
* - {py:obj}`TaggedConcept <research_vocabs.models.TaggedConcept>`
  -
````

### API

``````{py:class} Concept(*args, **kwargs)
:canonical: research_vocabs.models.Concept

Bases: {py:obj}`django.db.models.Model`

```{autodoc2-docstring} research_vocabs.models.Concept
```

```{rubric} Initialization
```

```{autodoc2-docstring} research_vocabs.models.Concept.__init__
```

````{py:attribute} label
:canonical: research_vocabs.models.Concept.label
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.Concept.label
```

````

````{py:attribute} URI
:canonical: research_vocabs.models.Concept.URI
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.Concept.URI
```

````

````{py:attribute} slug
:canonical: research_vocabs.models.Concept.slug
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.Concept.slug
```

````

````{py:attribute} scheme_label
:canonical: research_vocabs.models.Concept.scheme_label
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.Concept.scheme_label
```

````

````{py:attribute} scheme_URI
:canonical: research_vocabs.models.Concept.scheme_URI
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.Concept.scheme_URI
```

````

````{py:attribute} scheme_slug
:canonical: research_vocabs.models.Concept.scheme_slug
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.Concept.scheme_slug
```

````

`````{py:class} Meta
:canonical: research_vocabs.models.Concept.Meta

```{autodoc2-docstring} research_vocabs.models.Concept.Meta
```

````{py:attribute} verbose_name
:canonical: research_vocabs.models.Concept.Meta.verbose_name
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.Concept.Meta.verbose_name
```

````

````{py:attribute} verbose_name_plural
:canonical: research_vocabs.models.Concept.Meta.verbose_name_plural
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.Concept.Meta.verbose_name_plural
```

````

````{py:attribute} default_related_name
:canonical: research_vocabs.models.Concept.Meta.default_related_name
:value: >
   'keywords'

```{autodoc2-docstring} research_vocabs.models.Concept.Meta.default_related_name
```

````

````{py:attribute} unique_together
:canonical: research_vocabs.models.Concept.Meta.unique_together
:value: >
   ['label', 'scheme_URI']

```{autodoc2-docstring} research_vocabs.models.Concept.Meta.unique_together
```

````

`````

````{py:method} __str__()
:canonical: research_vocabs.models.Concept.__str__

````

````{py:method} save(*args, **kwargs)
:canonical: research_vocabs.models.Concept.save

````

````{py:method} add_concept(URI, scheme)
:canonical: research_vocabs.models.Concept.add_concept
:classmethod:

```{autodoc2-docstring} research_vocabs.models.Concept.add_concept
```

````

``````

``````{py:class} TaggedConcept(*args, **kwargs)
:canonical: research_vocabs.models.TaggedConcept

Bases: {py:obj}`django.db.models.Model`

````{py:attribute} object_id
:canonical: research_vocabs.models.TaggedConcept.object_id
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.TaggedConcept.object_id
```

````

````{py:attribute} content_type
:canonical: research_vocabs.models.TaggedConcept.content_type
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.TaggedConcept.content_type
```

````

````{py:attribute} content_object
:canonical: research_vocabs.models.TaggedConcept.content_object
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.TaggedConcept.content_object
```

````

````{py:attribute} concept
:canonical: research_vocabs.models.TaggedConcept.concept
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.TaggedConcept.concept
```

````

`````{py:class} Meta
:canonical: research_vocabs.models.TaggedConcept.Meta

```{autodoc2-docstring} research_vocabs.models.TaggedConcept.Meta
```

````{py:attribute} verbose_name
:canonical: research_vocabs.models.TaggedConcept.Meta.verbose_name
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.TaggedConcept.Meta.verbose_name
```

````

````{py:attribute} verbose_name_plural
:canonical: research_vocabs.models.TaggedConcept.Meta.verbose_name_plural
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.TaggedConcept.Meta.verbose_name_plural
```

````

````{py:attribute} indexes
:canonical: research_vocabs.models.TaggedConcept.Meta.indexes
:value: >
   None

```{autodoc2-docstring} research_vocabs.models.TaggedConcept.Meta.indexes
```

````

`````

````{py:property} concept_model
:canonical: research_vocabs.models.TaggedConcept.concept_model

```{autodoc2-docstring} research_vocabs.models.TaggedConcept.concept_model
```

````

````{py:method} create(content_object, URI, scheme)
:canonical: research_vocabs.models.TaggedConcept.create
:classmethod:

```{autodoc2-docstring} research_vocabs.models.TaggedConcept.create
```

````

``````
