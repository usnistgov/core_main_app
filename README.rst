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

Add the ``"core_main_app"`` and ``"tz_detect"`` under ``INSTALLED_APPS`` as
such:

.. code:: python

    INSTALLED_APPS = [
        ...
        "tz_detect",
        "core_main_app",
    ]

Add the middleware required by ``tz_detect``:

.. code:: python

    MIDDLEWARE = (
        ...
        'tz_detect.middleware.TimezoneMiddleware',
    )


Edit the urls.py file
---------------------

Add the ``core_main_app`` urls to the Django project as such.

.. code:: python

    url(r'^', include("core_main_app.urls")),


Internationalization (i18n)
===========================

Before running the project, don't forget to compile the translation file at
project level. i18n uses the ``gettext`` package, so please make sure it is
installed prior to using this command.

.. code:: bash

    $ python manage.py compilemessages

Tests
=====

To play the test suite created for this package, download the git repository
and run:

.. code:: bash

  $ python runtests.py

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

Enable SSL connection
=====================

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
==================================

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
==================

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