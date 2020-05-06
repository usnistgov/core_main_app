=============
Core Main App
=============

This file will give you information about the CDCS core frontend presentation and graphical design.

Libraries
=========

The core do not include preprocessor scripting language like sass or less.
All the libraries are written in CSS and JavaScript. Bootstrap is the main
library and is used in all the project. The Fontawesome library icons and some CSS utils are
used in the CDCS project. You can see below the version table of these two libraries:

+-----------------+-------------+---------------+
| CDCS versions   | Bootstrap   |  Fontawesome  |
+=================+=============+===============+
|    < 1.8.0      |     3.3.7   |     4.7.0     |
+-----------------+-------------+---------------+
|     1.9.0 >     |     4.4.1   |     5.13.0    |
+-----------------+-------------+---------------+

Migration
=========

Bootstrap migration to v4
-------------------------
Here is a link to help with the Bootstrap migration process:
https://getbootstrap.com/docs/4.0/migration/

* **Renamed .btn-default to .btn-secondary.**
* Some components and containers are rewritten with flexbox and consequently the
  behavior could change after the migration
* The list and pagination follow a new hierarchy and new names rules are added (.page-item, .page-link)
* We encourage the use of the flexbox Bootstrap tools for the layout https://getbootstrap.com/docs/4.0/utilities/flex/

Fontawesome migration to v5
---------------------------
Here is a link to help with the Fontawesome migration process:
https://fontawesome.com/how-to-use/on-the-web/setup/upgrading-from-version-4

* You can find a mapping table on the icon name changes between Version 4 and 5
* On the version 5 the wellknown "fa" is replaced by fas, fab, far, fal, fad
  to categorize the different icons (ex. fab mean Font Awesome Brands)
* **For the retro compatibility the fa prefix in an alias for fas** (Font Awesome Solid icons)
* The pull-right and pull-left utils classes are not available anymore, use the Bootstrap
  float-right and float-left classes instead