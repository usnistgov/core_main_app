=============
Core Main App
=============

This Django reusable app contains the main functionalities for the curator core project.

Pre-requisites
==============

* Install git
* Install python
* Install pip
* Create a virtual env

Installation
============

Automated installation
----------------------

.. warning::

    *The automated installation is not yet available.*

Manual installation
-------------------

.. code:: bash

    $ git clone https://myrepo.com/core_main_app.git
    $ cd core_main_app
    $ python setup.py
    $ pip install sdist/*.tar.gz


Configuration
=============

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


i18n
====

Before running the project, don't forget to compile the translation file at project level.
i18n uses the gettext package, so please make sure it is installed prior using this command.

.. code:: bash

    $ python manage.py compilemessages
