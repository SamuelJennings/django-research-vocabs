# Django Research Vocabs 

[![Github Build](https://github.com/SSJenny90/django-research-vocabs/actions/workflows/build.yml/badge.svg)](https://github.com/SSJenny90/django-research-vocabs/actions/workflows/build.yml)
[![Github Docs](https://github.com/SSJenny90/django-research-vocabs/actions/workflows/docs.yml/badge.svg)](https://github.com/SSJenny90/django-research-vocabs/actions/workflows/docs.yml)
[![CodeCov](https://codecov.io/gh/SSJenny90/django-research-vocabs/branch/main/graph/badge.svg?token=0Q18CLIKZE)](https://codecov.io/gh/SSJenny90/django-research-vocabs)
![GitHub](https://img.shields.io/github/license/SSJenny90/django-research-vocabs)
![GitHub last commit](https://img.shields.io/github/last-commit/SSJenny90/django-research-vocabs)
![PyPI](https://img.shields.io/pypi/v/django-research-vocabs)
<!-- [![RTD](https://readthedocs.org/projects/django-research-vocabs/badge/?version=latest)](https://django-research-vocabs.readthedocs.io/en/latest/readme.html) -->
<!-- [![Documentation](https://github.com/SSJenny90/django-research-vocabs/actions/workflows/build-docs.yml/badge.svg)](https://github.com/SSJenny90/django-research-vocabs/actions/workflows/build-docs.yml) -->
<!-- [![PR](https://img.shields.io/github/issues-pr/SSJenny90/django-research-vocabs)](https://github.com/SSJenny90/django-research-vocabs/pulls)
[![Issues](https://img.shields.io/github/issues-raw/SSJenny90/django-research-vocabs)](https://github.com/SSJenny90/django-research-vocabs/pulls) -->
<!-- ![PyPI - Downloads](https://img.shields.io/pypi/dm/django-research-vocabs) -->
<!-- ![PyPI - Status](https://img.shields.io/pypi/status/django-research-vocabs) -->

A scientific keywords management app for Django

Documentation
-------------

The full documentation is at https://ssjenny90.github.io/django-research-vocabs/

Quickstart
----------

Install Django Research Vocabs::

    pip install django-research-vocabs

Add it to your `INSTALLED_APPS`:


    INSTALLED_APPS = (
        ...
        'keywords',
        ...
    )

Add Django Research Vocabs's URL patterns:

    urlpatterns = [
        ...
        path('', include("keywords.urls")),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

