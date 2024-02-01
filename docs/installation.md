# Installation

```{note}

If you are developing within the Geoluminate ecosystem, you can skip this step as this package is pre-installed with the core `geoluminate-package` virtual environment.

```

Using pip...

    pip install django-research-vocabs

...or Poetry

    poetry add django-research-vocabs


If you would like to use the `TaggableConcept` feature for generic tagging of research concepts, you will need to add `django-research-vocabs` to your `INSTALLED_APPS`.

    INSTALLED_APPS = (
        ...
        'research_vocabs',
        ...
    )
