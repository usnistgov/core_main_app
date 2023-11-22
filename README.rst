=============
Core Main App
=============

This Django reusable app contains the main functionalities for the curator
core project.

Pre-requisites
==============

For automated and manual install, the following software are needed:

* ``python``
* ``pip``
* virtual env (``conda`` or ``venv``)

In addition, for manual setup, ``git`` is needed.

Installation
============

Automated installation
----------------------

.. code:: bash

  $ pip install core_main_app

Manual installation
-------------------

.. code:: bash

    $ git clone https://github.com/usnistgov/core_main_app.git
    $ cd core_main_app
    $ python setup.py
    $ pip install sdist/*.tar.gz


Configuration
=============

Edit the setting.py file
------------------------

Add the ``"core_main_app"`` under ``INSTALLED_APPS`` as
such:

.. code:: python

    INSTALLED_APPS = [
        ...
        "core_main_app",
    ]


Edit the urls.py file
---------------------

Add the ``core_main_app`` urls to the Django project as such.

.. code:: python

    url(r'^', include("core_main_app.urls")),


Internationalization (i18n)
---------------------------

Before running the project, don't forget to compile the translation file at
project level. i18n uses the ``gettext`` package, so please make sure it is
installed prior to using this command.

.. code:: bash

    $ python manage.py compilemessages

Enable SSL connection
---------------------

Please follow these steps to configure the connection to any system running over HTTPS (including the local instance).

* Create a folder for SSL certificates,
* Copy the certificate in the folder,
* Run ``c_rehash`` on the folder (needs to be done every time a new certificate is added to the folder),
* Update the SSL_CERTIFICATES_DIR setting to point to the SSL certificate folder previously created.

.. code:: bash

  $ mkdir certs
  $ cp cdcs.crt certs/
  $ c_rehash certs/

Enable Redis Server authentication
----------------------------------

Please follow these steps to enable authentication on the redis server.
Depending on the way Redis is started on the machine, the method may differ.

You can follow instructions at https://redis.io/topics/security#authentication-feature to enable authentication:
* Open the file redis.conf (e.g. /usr/local/etc/redis.conf),
* Uncomment the authentication setting (# requirepass foobared),
* It is recommended to replace the default password (foobared) by a strong and long password,
* Restart the Redis Server.

You should then update the CDCS settings using a Redis connection URL with the password chosen in the previous steps.

.. code:: python

  BROKER_URL = 'redis://:<password>@localhost:6379/0'
  CELERY_RESULT_BACKEND = 'redis://:<password>@localhost:6379/0'


Enable SMTP server
------------------

Please follow these steps to configure the SMTP server:

* Set these constants in your setting.py file (all these constants are required)

.. code:: py

  EMAIL_HOST = 'smtp.myserver.com'
  EMAIL_PORT = 587
  DEFAULT_FROM_EMAIL = 'TestSite Team <noreply@example.com>'


* These optional constants can be added in your setting.py according to your SMTP server configuration

.. code:: py

  EMAIL_USE_TLS = True
  EMAIL_HOST_USER = 'testsite_app'
  EMAIL_HOST_PASSWORD = 'mys3cr3tp4ssw0rd'

Enable History
--------------

Django Simple History allows keeping track of changes made to an object stored in the CDCS database.
First, install and configure the package. See the
`django-simple-history <https://django-simple-history.readthedocs.io/en/latest/quick_start.html>`_ documentation.

Then, set the `DJANGO_SIMPLE_HISTORY_MODELS` setting with a list of models to track.
At the moment, this feature is only available for the `Data` model.

.. code:: python

  DJANGO_SIMPLE_HISTORY_MODELS=["Data"]

Register models to track by updating project files.
For example in ``mdcs/mdcs_home/admin.py``, add the following lines:

.. code:: python

  from core_main_app.utils.admin_site.model_admin_class import register_simple_history_models
  from django.conf import settings

  DJANGO_SIMPLE_HISTORY_MODELS = getattr(settings, "DJANGO_SIMPLE_HISTORY_MODELS", None)
  register_simple_history_models(DJANGO_SIMPLE_HISTORY_MODELS)

Documentation
=============

Documentation has been generated using Sphinx. To generate a local version of
the docs, please clone the repository and run:

.. code:: bash

  $ cd docs/
  $ make html

Or, directly using Sphinx:

.. code:: bash

  $ cd docs/
  $ sphinx-build -b html . ../dist/_docs

Development
===========

Development version
-------------------

A development version of this package is available, containing tests and formatting
dependencies. To automatically install the development version, run:

.. code:: bash

  $ pip install .[develop]

The development dependencies are located in ``requirements.dev.txt`` and can be installed
manually using:

.. code:: bash

  $ pip install -r requirements.dev.txt

Code formatting
---------------

To ensure consistent formatting across the codebase, the development team is using
`black <https://github.com/psf/black>`_. When contributing to this package, install black
as part of the development packages and run ``black /path/to/core_main_app`` before
submitting the contribution.

Tests
-----

To play the test suite created for this package, download the git repository, install the
development dependencies and run:

.. code:: bash

  $ python runtests.py

Sending email
-------------

To test the email being sent, console backend will print the email instead of sending the real email.
By default, the console backend writes to stdout

To specify this backend, add the following in your settings:

.. code:: python

  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

JSON Support
------------

CDCS 2.6 adds the ability to work directly with JSON documents. A Template can now either be
an XML Schema or a JSON schema. Uploaded data, in XML or JSON format, will be validated by a template in
the corresponding format, by the appropriate validator.

This addition has been implemented as an option and needs to be enabled to make the features appear in the system.
The following settings have been added with the implementation of JSON support and need to be set properly to enable the
feature.

.. code:: python

  ENABLE_JSON_SCHEMA_SUPPORT = True
  BACKWARD_COMPATIBILITY_DATA_XML_CONTENT = False
  ALLOW_MULTIPLE_SCHEMAS = True # only required for registries

To enable JSON support in the CDCS, ``ENABLE_JSON_SCHEMA_SUPPORT`` should be set to ``True``. For the registry projects,
which are limited to a single XML Schema by default, the setting ``ALLOW_MULTIPLE_SCHEMAS`` should also be set to
``True``.
Before CDCS 2.6, some fields of the database contained direct references to the XML format. In particular, the property
to read the content of an XML data was called ``xml_content``. When adding support for new formats, these fields have
been renamed to not be tied to a specific format, thus ``Data.xml_content`` was renamed ``Data.content``. The change also
impacted REST APIs, and data upload would need to set a ``content`` field, and responses would return a ``content``
field. For users that are not ready to migrate their scripts to the new configuration yet, a setting has been added to
continue accepting ``xml_content`` instead of ``content`` in the REST API. It is recommended to set
``BACKWARD_COMPATIBILITY_DATA_XML_CONTENT`` to ``False`` when ready to make the move to JSON Support and start using
``Data.content``.
