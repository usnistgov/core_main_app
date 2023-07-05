Bootstrap Version Upgrade Guide
===============================

The CDCS is now able to support several versions of the Bootstrap library, to make the transition smoother.

Make sure to review the `Official Bootstrap documentation <https://getbootstrap.com/docs/5.0/migration/>`_

Bootstrap Version
-----------------

Before making any changes, ensure that you have identified the version of Bootstrap used in your project. You can find this information with the BOOTSTRAP_VERSION variable.

* ``Version compatibility matrix``

+---------------------+----------------------+
|       core 2.3      |          4.6.2       |
+---------------------+----------------------+
|       core 2.4      |    4.6.2 / 5.1.3     |
+---------------------+----------------------+



Conditional Classes/Attributes
------------------------------

* ``Syntax``

Conditional checks were added to some HTML tags in order to differentiate between Bootstrap 4 and 5 classes and attributes:

.. code-block:: html

   {% if BOOTSTRAP_VERSION == "4.6.2" %}
    Use Bootstrap old classes/attributes

   {% elif BOOTSTRAP_VERSION == "5.1.3" %}
    Use Bootstrap new classes/attributes

   {% endif %}



* ``Attributes``

Update data attributes by replacing the corresponding Bootstrap 4 and 5 data attribute.

data-attribute  becomes data-bs-attribute  :


+------------------+--------------------+
|       BS_v4      |         BS_v5      |
+==================+====================+
|   data-dismiss   |   data-bs-dismiss  |
+------------------+--------------------+
|  data-parent     |   data-bs-parent   |
+------------------+--------------------+
|   data-toggle    | data-bs-toggle     |
+------------------+--------------------+
|  data-placement  | data-bs-placement  |
+------------------+--------------------+


Example:

    .. code-block:: html

        <button type="submit"
        {% if BOOTSTRAP_VERSION == "4.6.2" %}data-dismiss{% elif BOOTSTRAP_VERSION == "5.1.3" %}data-bs-dismiss{% endif %}="modal"/>



* ``Classes``

Replace the existing class names with the appropriate Bootstrap 4 or Bootstrap 5 class name based on the conditional statements provided bellow.

Class names :


+------------------------+---------------------+
|         BS_v4          |         BS_v5       |
+========================+=====================+
|     custom-control     |    form-control     |
+------------------------+---------------------+
|     custom-switch      |     form-switch     |
+------------------------+---------------------+
|   custom-control-input | form-control-input  |
+------------------------+---------------------+
|  custom-control-label  | form-control-label  |
+------------------------+---------------------+
|     float-right        |    float-end        |
+------------------------+---------------------+
|     float-left         |     float-start     |
+------------------------+---------------------+
|   float-right          | float-end           |
+------------------------+---------------------+
|   text-left            | text-start          |
+------------------------+---------------------+
|         close          |     btn-close       |
+------------------------+---------------------+
|          mr            |         me          |
+------------------------+---------------------+
|          ml            |         ms          |
+------------------------+---------------------+
|          pr            |         pe          |
+------------------------+---------------------+
|          pl            |         ps          |
+------------------------+---------------------+



Example:

    .. code-block:: html

        <div class="{% if BOOTSTRAP_VERSION == "4.6.2" %}float-right{% elif BOOTSTRAP_VERSION == "5.1.3" %}float-end{% endif %}"
            ...
        </div>