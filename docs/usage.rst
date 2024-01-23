=====
Usage
=====

To use Django Research Vocabs in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'keywords.apps.KeywordsConfig',
        ...
    )

Add Django Research Vocabs's URL patterns:

.. code-block:: python

    from keywords import urls as keywords_urls


    urlpatterns = [
        ...
        url(r'^', include(keywords_urls)),
        ...
    ]
