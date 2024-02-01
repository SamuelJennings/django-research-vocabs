# {py:mod}`research_vocabs.forms`

```{py:module} research_vocabs.forms
```

```{autodoc2-docstring} research_vocabs.forms
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`KeywordFieldBase <research_vocabs.forms.KeywordFieldBase>`
  - ```{autodoc2-docstring} research_vocabs.forms.KeywordFieldBase
    :summary:
    ```
* - {py:obj}`KeywordChoiceField <research_vocabs.forms.KeywordChoiceField>`
  - ```{autodoc2-docstring} research_vocabs.forms.KeywordChoiceField
    :summary:
    ```
* - {py:obj}`KeywordMultiChoiceField <research_vocabs.forms.KeywordMultiChoiceField>`
  - ```{autodoc2-docstring} research_vocabs.forms.KeywordMultiChoiceField
    :summary:
    ```
* - {py:obj}`KeywordModelChoiceField <research_vocabs.forms.KeywordModelChoiceField>`
  - ```{autodoc2-docstring} research_vocabs.forms.KeywordModelChoiceField
    :summary:
    ```
* - {py:obj}`KeywordFormMixin <research_vocabs.forms.KeywordFormMixin>`
  - ```{autodoc2-docstring} research_vocabs.forms.KeywordFormMixin
    :summary:
    ```
* - {py:obj}`KeywordForm <research_vocabs.forms.KeywordForm>`
  -
* - {py:obj}`KeywordModelForm <research_vocabs.forms.KeywordModelForm>`
  -
````

### API

`````{py:class} KeywordFieldBase(scheme='', *args, **kwargs)
:canonical: research_vocabs.forms.KeywordFieldBase

```{autodoc2-docstring} research_vocabs.forms.KeywordFieldBase
```

```{rubric} Initialization
```

```{autodoc2-docstring} research_vocabs.forms.KeywordFieldBase.__init__
```

````{py:method} clean(value)
:canonical: research_vocabs.forms.KeywordFieldBase.clean

```{autodoc2-docstring} research_vocabs.forms.KeywordFieldBase.clean
```

````

`````

````{py:class} KeywordChoiceField(scheme='', *args, **kwargs)
:canonical: research_vocabs.forms.KeywordChoiceField

Bases: {py:obj}`research_vocabs.forms.KeywordFieldBase`, {py:obj}`django.forms.ChoiceField`

```{autodoc2-docstring} research_vocabs.forms.KeywordChoiceField
```

```{rubric} Initialization
```

```{autodoc2-docstring} research_vocabs.forms.KeywordChoiceField.__init__
```

````

````{py:class} KeywordMultiChoiceField(scheme='', *args, **kwargs)
:canonical: research_vocabs.forms.KeywordMultiChoiceField

Bases: {py:obj}`research_vocabs.forms.KeywordFieldBase`, {py:obj}`django.forms.MultipleChoiceField`

```{autodoc2-docstring} research_vocabs.forms.KeywordMultiChoiceField
```

```{rubric} Initialization
```

```{autodoc2-docstring} research_vocabs.forms.KeywordMultiChoiceField.__init__
```

````

`````{py:class} KeywordModelChoiceField(scheme='', *args, **kwargs)
:canonical: research_vocabs.forms.KeywordModelChoiceField

Bases: {py:obj}`research_vocabs.forms.KeywordFieldBase`, {py:obj}`django.forms.ModelChoiceField`

```{autodoc2-docstring} research_vocabs.forms.KeywordModelChoiceField
```

```{rubric} Initialization
```

```{autodoc2-docstring} research_vocabs.forms.KeywordModelChoiceField.__init__
```

````{py:method} limit_choices()
:canonical: research_vocabs.forms.KeywordModelChoiceField.limit_choices

```{autodoc2-docstring} research_vocabs.forms.KeywordModelChoiceField.limit_choices
```

````

````{py:method} to_python(value)
:canonical: research_vocabs.forms.KeywordModelChoiceField.to_python

````

`````

`````{py:class} KeywordFormMixin(*args, **kwargs)
:canonical: research_vocabs.forms.KeywordFormMixin

```{autodoc2-docstring} research_vocabs.forms.KeywordFormMixin
```

```{rubric} Initialization
```

```{autodoc2-docstring} research_vocabs.forms.KeywordFormMixin.__init__
```

````{py:method} clean()
:canonical: research_vocabs.forms.KeywordFormMixin.clean

```{autodoc2-docstring} research_vocabs.forms.KeywordFormMixin.clean
```

````

````{py:method} _clean_keywords()
:canonical: research_vocabs.forms.KeywordFormMixin._clean_keywords

```{autodoc2-docstring} research_vocabs.forms.KeywordFormMixin._clean_keywords
```

````

`````

```{py:class} KeywordForm(*args, **kwargs)
:canonical: research_vocabs.forms.KeywordForm

Bases: {py:obj}`research_vocabs.forms.KeywordFormMixin`, {py:obj}`django.forms.Form`

```

`````{py:class} KeywordModelForm(*args, **kwargs)
:canonical: research_vocabs.forms.KeywordModelForm

Bases: {py:obj}`research_vocabs.forms.KeywordFormMixin`, {py:obj}`django.forms.ModelForm`

````{py:method} save(commit=True)
:canonical: research_vocabs.forms.KeywordModelForm.save

````

````{py:method} _save_m2m()
:canonical: research_vocabs.forms.KeywordModelForm._save_m2m

```{autodoc2-docstring} research_vocabs.forms.KeywordModelForm._save_m2m
```

````

`````
