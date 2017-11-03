core_main_app
=============

Main functionalities for the curator core project.

Quick start
===========

1. Add "core_main_app" to your INSTALLED_APPS setting like this
---------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
        ...
        "core_main_app",
    ]

2. Include the core_main_app URLconf in your project urls.py like this
----------------------------------------------------------------------

.. code:: python

    url(r'^', include("core_main_app.urls")),
