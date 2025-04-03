# Settings

This document lists all the available settings for CDCS core applications.
Additional settings can be used to configure other Django packages used in the CDCS, such as:

- [Django Settings](https://docs.djangoproject.com/en/4.2/ref/settings/),
- 3rd party packages settings ([DRF](https://www.django-rest-framework.org/api-guide/settings/), [django-defender](https://django-defender.readthedocs.io/en/latest/#customizing-django-defender),...)

## Server Configuration

### ``SERVER_URI``

  Default: ``"http://localhost:8000"``

  URI of the web server.

### ``CUSTOM_NAME``

  Default: ``"Local"``

  Name of the local CDCS instance.

### ``PROJECT_VERSION``

  Default: ``"0.0.0"``

  Version number of the project.


## Databases

Settings for extra database configuration.
This is a complement and not a substitute for [Django database settings](https://docs.djangoproject.com/en/4.2/ref/settings/#database).

**MongoDB**
***********

These settings should be set when using MongoDB for data indexing and/or GridFS for file storage.

### ``MONGO_HOST``

  Default: ``"localhost"``

  MongoDB host.

### ``MONGO_PORT``

  Default: ``"27017"``

  MongoDB port.

### ``MONGO_USER``

  Default: ``""``

  MongoDB user.

### ``MONGO_PASS``

  Default: ``""``

  MongoDB password.

### ``MONGO_DB``

  Default: ``cdcs``

  MongoDB database.

### ``MONGODB_INDEXING``

  Default: ``False``

  If ``True``, MongoDB will be used for data indexing and queries will be executed against MongoDB by default.

### ``MONGODB_ASYNC_SAVE``

  Default: ``True``

  Save data in MongoDB asynchronously.


## File Storage

### ``GRIDFS_STORAGE``

  Default: ``False``

  Set to ``True`` to use GridFS for file storage.

### ``CUSTOM_FILE_STORAGE``

  Default: ``{}``

  File Storage by model.

  Example:

  ```python
from django.core.files.storage import default_storage
{
    'data': default_storage,
    'template': default_storage,
    'xsl_transformation': default_storage,
    'blob': 'core_main_app.utils.storage.gridfs_storage.GridFSStorage',
    'exported_compressed_files': 'core_main_app.utils.storage.gridfs_storage.GridFSStorage',
}
  ```

> :page_facing_up: ``GRIDFS_STORAGE`` needs to be set to ``True`` to be able to use it here.


> :warning: Please read Django notes regarding [user-uploaded content](https://docs.djangoproject.com/en/4.2/topics/security/#user-uploaded-content)
> and [additional security topics](https://docs.djangoproject.com/en/4.2/topics/security/#additional-security-topics)
> when choosing the default file system storage.

### ``CHECKSUM_ALGORITHM``

  Default: ``None``

  Checksum algorithm used for uploaded files.
  Choose from: None, "MD5", "SHA1", "SHA256", "SHA512".

## Access Control


### ``CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT``

  Default: ``False``

  Can anonymous users (not logged in) access public document.

### ``CAN_SET_WORKSPACE_PUBLIC``

  Default: ``True``

  Can users switch private workspaces to public.

### ``CAN_SET_PUBLIC_DATA_TO_PRIVATE``

  Default: ``True``

  Set to ``True`` if public data can be unpublished.

### ``VERIFY_DATA_ACCESS``

  Default: ``False``

  Verify that data returned by a query can be accessed.
  CDCS queries are prepared to only return data that the user can access.
  If ``True``, the list of returned data will also be checked. This extra check can be slow.


## Data Exploration

**Queries**
***********

### ``RESULTS_PER_PAGE``

  Default: ``10``

  Number of records to display per page.

### ``DATA_SOURCES_EXPLORE_APPS``

  Default: ``[]``

  Example:

```python
DATA_SOURCES_EXPLORE_APPS = [
    'core_explore_federated_search_app',
    'core_explore_oaipmh_app',
]
```

> :page_facing_up: Applications added to this list need to be properly installed and configured.

### ``EXPLORE_ADD_DEFAULT_LOCAL_DATA_SOURCE_TO_QUERY``

  Default: ``True``

  Set to ``True`` to execute queries on the local instance by default (without explicitly selecting it).

### ``QUERIES_MAX_DAYS_IN_DATABASE``

  Default: ``7``

  Number of days after which temporary queries object are removed from database.

### ``QUERY_VISIBILITY``

  Default: ``VISIBILITY_PUBLIC``

  Set to ``VISIBILITY_PUBLIC`` to return only public data in exploration apps.

> :page_facing_up: This setting is used by registry projects. Data repositories on the other hand, 
> return all accessible data to a user by default.

### ``DATA_DISPLAYED_SORTING_FIELDS``

  Default:

```python
[
    {"field": "title", "display": "Title"},
    {"field": "last_modification_date", "display": "Last modification date"},
    {"field": "template", "display": "Template"},
]
```

  Sorting fields displayed on the search pages.

### ``DEFAULT_DATE_TOGGLE_VALUE``

  Default: ``False``

  Set the default value for the toggle component that controls the display of the modification date
  of each record on the search page.

### ``DISPLAY_EDIT_BUTTON``

  Default: ``False``

  Set to ``True`` to display an edit button next to each record the user is allowed to edit,
  directly on the search page.

### ``SORTING_DISPLAY_TYPE``

  Default: ``"single"``

  Result sorting display type. Choose between single criteria (``"single"``) or multiple criteria (``"multi"``) sorting.

### ``EXPLORE_KEYWORD_APP_EXTRAS``

  Default: ``[]``

  List of additional resources (html/css/js) to load on the exploration page.

> :page_facing_up: This option can be used to modify or add components on the exploration page, 
> without overriding the existing templates.

### ``DATA_SORTING_FIELDS``

  Default: ``[]``

  Default sorting fields for the data. All the field must be prefixed by "+" or "-" (ascending or descending order)

  Example:

```python
DATA_SORTING_FIELDS = ["-title", "+last_modification_date"]
```
      


### ``SEARCHABLE_DATA_OCCURRENCES_LIMIT``

  Default: ``None``

  Set to an integer to limit the number of array elements to index.


**Export**
**********

### ``EXPORTED_COMPRESSED_FILE_FOLDER``

  Default: ``"exporter_compressed_files"``

  Name of folder used to store compressed files generated by exporters.

### ``COMPRESSED_FILES_EXPIRE_AFTER_SECONDS``

  Default: ``10``

  Number of seconds after which exported files are deleted.

## Dashboard

### ``FORM_PER_PAGE_PAGINATION``

  Default: ``"RESULTS_PER_PAGE"``

  Customize the number of forms displayed per page

### ``RECORD_PER_PAGE_PAGINATION``

  Default: ``"RESULTS_PER_PAGE"``

  Customize the number of records displayed per page

### ``FILE_PER_PAGE_PAGINATION``

  Default: ``"RESULTS_PER_PAGE"``

  Customize the number of files displayed per page

### ``QUERY_PER_PAGE_PAGINATION``

  Default: ``"RESULTS_PER_PAGE"``

  Customize the number of queries displayed per page


## UI Customization

### ``WEBSITE_ADMIN_COLOR``

  Default: ``"yellow"``

  Color of the admin dashboard. black, black-light, blue, blue-light, green, green-light, purple, purple-light, red,
  red-light, yellow, yellow-light.

### ``DISPLAY_NIST_HEADERS``

  Default: ``False``

  Set to ``True`` to show the NIST headers and footers on all pages.


### ``CURATE_MENU_NAME``

  Default: ``"Curator"``

  label for the data curation app menu.


### ``EXPLORE_EXAMPLE_MENU_NAME``

  Default: ``"Query by Example"``

  label for the explore by example app menu.


### ``EXPLORE_MENU_NAME``

  Default: ``"Query by Keyword"``

  label for the explore by keyword app menu.


### ``TEXT_EDITOR_LIBRARY``

  Default: ``"Monaco"``

  Customize the type of editor used within the  app. Choose between  None and "Monaco" and other third-party text editors:
  - 'None' to use the simple text editor with minimal features.
  - 'Monaco' to use Monaco editor for advanced code editing capabilities.
  - Set parameter to the name of the desired third-party text editor to integrate.


## XML

### ``XSD_UPLOAD_DIR`` (> :warning: Deprecated)

  Default: ``"xml_schemas"``

  Name of the media folder where XML schemas are uploaded to.

### ``XSLT_UPLOAD_DIR`` (> :warning: Deprecated)

  Default: ``"xslt"``

  Name of the media folder where XML schemas are uploaded to.

### ``DEFAULT_DATA_RENDERING_XSLT``

  Default: ``"core_main_app/common/xsl/xml2html.xsl"``

  Path to default XSLT to render data.

### ``PARSER_MIN_TREE``

  Default: ``True``

  Generate minimal version of the XML tree (elements with ``minOccurs=0`` are not generated, but can be added later).

### ``PARSER_IGNORE_MODULES``

  Default: ``False``

  Set to ``True`` to generate XML tree without UI modules.

### ``PARSER_COLLAPSE``

  Default: ``True``

  Set to ``True`` to allow collapsing sections of the XML Tree.

### ``PARSER_IMPLICIT_EXTENSION_BASE``

  Default: ``False``

  Set to ``True`` to add the base type of an extension and render it alone without extensions.

### ``PARSER_DOWNLOAD_DEPENDENCIES``

  Default: ``False``

  Set to ``True`` to allow parser download imports.

### ``PARSER_MAX_IN_MEMORY_ELEMENTS``

  Default: 10000

  Maximum number of in-memory elements to be generated during the parsing of an XML document.
  An error is raised when the limit is reached.

### ``MAX_DOCUMENT_EDITING_SIZE``

  Default: 128 * 1024

  Maximum size of XML documents being edited in the browser (in bytes).

### ``XSD_URI_RESOLVER``

  Default: ``None``

  XSD URI Resolver for lxml validation. Choose from:  None, "REQUESTS_RESOLVER" (pass user information from
  the request to CDCS apis).

### ``XML_FORCE_LIST``

  Default: ``False``

  force_list parameter for xmltodict.parse function (used for XML to JSON conversion).
  Choose between a boolean, a list of elements to convert to list or a callable:
  - boolean: convert or not xml elements to list,
  - list: list of xml element that need to be converted to a list,
  - callable: for other custom force_list behavior.

### ``XML_POST_PROCESSOR``

  Default: ``"NUMERIC"``

  postprocessor parameter for xmltodict.parse function (used for XML to JSON conversion).
  Choose between 'NUMERIC' and 'NUMERIC_AND_STRING' or a callable.
  - 'NUMERIC' convert numeric values from the xml document to integer or float,
  - 'NUMERIC_AND_STRING' convert numeric values and also store string representation,
  - callable for other custom xml post processing.

### ``MODULE_TAG_NAME``

  Default: ``"module"``

  Name of the XML tag used to store module information.


### ``AUTO_ESCAPE_XML_ENTITIES``

  Default: ``True``

  Set to ``True`` to auto escape of the XML predefined entities when saving data.

### ``ENABLE_XML_ENTITIES_TOOLTIPS``

  Default: ``True``

  Set to ``True`` to display a warning when XML predefined entities are found in the data entry form.


## Registry

### ``XSL_FOLDER_PATH``

  Default: ``"core_explore_keyword_registry_app/xsl"``

  Path to folder containing XSLT files used for the initialisation.

### ``LIST_XSL_FILENAME``

  Default: ``"registry-list.xsl"``

  Name of XSLT file used to render a page of search results (loaded during initialisation).

### ``DETAIL_XSL_FILENAME``

  Default: ``"registry-detail.xsl"``

  Name of XSLT file used to render a single record (loaded during initialisation).

### ``REGISTRY_XSD_FILEPATH``

  Default: ``"core_main_registry_app/xsd/res-md.xsd"``

  Path to the resource template (loaded during initialisation).

### ``REGISTRY_XSD_FILENAME``

  Default: ``""``

  Name of the resource template (loaded during initialisation).

### ``REGISTRY_XSD_USER_FILEPATH``

  Default: ``"core_user_registration_app/user/xsd/user.xsd"``

  Path to the user registration template (loaded during initialisation).

### ``REGISTRY_XSD_USER_FILENAME``

  Default: ``"user.xsd"``

  Name of the user registration template (loaded during initialisation).

### ``CUSTOM_REGISTRY_FILE_PATH``

  Default: ``"core_main_registry_app/json/custom_registry.json"``

  Path to custom registry configuration file (loaded during initialisation).

### ``ENABLE_BLOB_ENDPOINTS``

  Default: ``False``

  Set to ``True`` to enable blob api and user views for blob management.

### ``ENABLE_BLOB_MODULES_SIGNALS``

  Default: ``True``
  
  Set to `True` to enable Blob modules signals (will trigger some actions on blob create/update/delete)

### ``LOCAL_ID_LENGTH``

  Default: ``20``

  Length of the unique local id to be stored in resource data.

> :page_facing_up: This setting is only useful when not using the persistent identifiers.

### ``ALLOW_MULTIPLE_SCHEMAS``

  Default: ``False``

  Allow the upload of more than one schema in the registry.


## OAI-PMH

### ``OAI_ENABLE_HARVESTING``

  Default: ``False``

  Set to ``True`` to enable harvesting by default.

### ``WATCH_REGISTRY_HARVEST_RATE``

  Default: ``60``

  Harvesting rate in seconds.

## Authentication

### ``ADMIN_URLS_PREFIX``

  Default: ``staff-``

  Prefix added to admin urls. Should be set to a unique string per system and kept secret.


### ``ENABLE_ALLAUTH``

  Default: ``False``

  Set to ``True`` to enable the `django-allauth` package.
  Install the required packages `core-main-app[allauth]` to do so.

### ``ENABLE_SAML2_SSO_AUTH``

  Default: ``False``

  Set to ``True`` to enable SAML2 SSO Authentication.
  If ENABLE_ALLAUTH is ``True``, SAML2 will be done with `django-allauth`,
  Otherwise, SAML2 will be done with `djangosaml2`.

### ``ENABLE_LOCAL_MFA``

  Default: ``False``

  Set to ``True`` to enable local MFA using `django-allauth`.

### ``SAML_EMAIL_AUTHENTICATION``

  Default: ``False``

  Set to ``True`` to allow authentication using a matching email address
  from a trusted Identity Provider.

### ``SAML_VERIFIED_EMAIL``

  Default: ``False``

  Set to ``True`` to ensure email address(es) retrieved from the provider are to be 
  interpreted as verified. Can be set to a list of accepted domains:

  Example:

```
SAML_VERIFIED_EMAIL=example.com,test.example.com
```

## EMAILS

### ``EMAIL_HOST``

  Default: ``localhost``

  The host to use for sending email.
  https://docs.djangoproject.com/en/4.2/ref/settings/#email-host

### ``EMAIL_PORT``

  Default: 25

  Port to use for the SMTP server defined in EMAIL_HOST.
  https://docs.djangoproject.com/en/4.2/ref/settings/#email-port

### ``DEFAULT_FROM_EMAIL``

  Default: ``webmaster@localhost``

  Default email address to use for various automated correspondence from the site manager(s). 
  This doesn’t include error messages sent to ADMINS and MANAGERS; for that, see SERVER_EMAIL.
  https://docs.djangoproject.com/en/4.2/ref/settings/#default-from-email

### ``EMAIL_SUBJECT_PREFIX``

  Default: ``[CURATOR]``

  Subject-line prefix for email messages.
  https://docs.djangoproject.com/en/4.2/ref/settings/#email-subject-prefix

### ``SERVER_EMAIL``

  Default: ``root@localhost``

  The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
  https://docs.djangoproject.com/en/4.2/ref/settings/#server-email

### ``ADMINS``
  
  Default: ``[]``

  A list of all the people who get code error notifications. 
  https://docs.djangoproject.com/en/4.2/ref/settings/#admins

### ``MANAGERS``

  Default: ``[]``

  A list of all the people that should get broken link notifications
  https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-MANAGERS

### ``WEBSITE_CONTACTS``

  Default: ``[]``

  A list of all the people who get notified when contact messages,
  or account requests are sent via the application.

  Example:

```
WEBSITE_CONTACTS = [("John", "john@example.com"), ("Mary", "mary@example.com")]
```

### ``SEND_EMAIL_ASYNC``

  Default: ``"False"``

  Set to ``True`` to send emails asynchronously.

### ``SEND_EMAIL_WHEN_CONTACT_MESSAGE_IS_RECEIVED``

  Default: ``False``

  Set to ``True`` to email the website contacts when a contact message is received.

### ``SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_ACCEPTED``

  Default: ``False``

  Set to ``True`` to email the person who requested an account when the account request is accepted.

### ``SEND_EMAIL_WHEN_ACCOUNT_REQUEST_IS_DENIED``

  Default: ``False``

  Set to ``True`` to email the person who requested an account when the account request is denied.

### ``EMAIL_DENY_SUBJECT``

  Default: ``"Account request denied"``

  Set the email subject sent to the person whose account request is being denied.


> :page_facing_up: More information can be found on the Django documentation for
    [sending emails](https://docs.djangoproject.com/en/4.2/topics/email/).

## Miscellaneous

### ``PASSWORD_RESET_DOMAIN_OVERRIDE``

  Default: ``None``

  Override domain of reset password email (e.g. localhost:8000)

### ``LOCK_OBJECT_TTL``

  Default: ``600``

  Data editing lock duration in seconds.

### ``SSL_CERTIFICATES_DIR``

  Default: ``True``

  SSL certificates directory location.

> :page_facing_up: This setting is used for the 'verify' parameter when using the python requests package.
    More information can be found in the [SSL Cert Verification](https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification) section.

### ``BOOTSTRAP_VERSION``

  Default: ``4.6.2``

  Version of the bootstrap library. Choose from the list of available bootstrap versions:
  - '4.6.2'
  - '5.1.3' 
  - '5.3.1'

### ``DJANGO_SIMPLE_HISTORY_MODELS``

  Default: ``None``

  Track history of listed models. Limited to `Data` for now.

### ``ENABLE_JSON_SCHEMA_SUPPORT``

  Default: ``False``

  From `core_main_app==2.6`, support for JSON Schema and Data has been implemented.
  Set to `True` to enable this feature.

### ``BACKWARD_COMPATIBILITY_DATA_XML_CONTENT``

  Default: ``True``

  From `core_main_app==2.6`, support for JSON Schema and Data has been implemented,
  and the field `Data.xml_content` has been renamed `Data.content`.
  Set to `True` to continue using `Data.xml_content` (deprecated) instead of `Data.content` in the REST API.


## Deployment

Additional deployment settings can be found on the CDCS docker repository:
- [SAML2](https://github.com/usnistgov/cdcs-docker#saml2),
- [Persistent identifiers](https://github.com/usnistgov/cdcs-docker#hdlnet-pid-integration).

