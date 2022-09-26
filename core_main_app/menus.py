""" Menu configuration for core_main_app.
Upon installation of the app the following menus are displayed:

  * User menu

    * Home

  * Admin menu

    * Dashboard
    * Link to Django admin
    * Login message
    * Templates (list and upload)
    * XSLT (list and upload)
"""
from django.urls import reverse
from menu import Menu, MenuItem

Menu.add_item(
    "main",
    MenuItem(
        "Home", reverse("core_main_app_homepage"), icon="home", weight=-1000
    ),
)

Menu.add_item(
    "admin",
    MenuItem(
        "Dashboard",
        reverse("core-admin:core_main_app_admin_home"),
        icon="tachometer-alt",
        weight=-90000,
    ),
)

Menu.add_item(
    "admin",
    MenuItem(
        "Django admin", reverse("admin:index"), icon="sitemap", weight=-80000
    ),
)

Menu.add_item(
    "admin",
    MenuItem(
        "Login message",
        reverse("core-admin:core_main_app_login_page"),
        icon="file-alt",
        weight=-70000,
    ),
)

templates_children = (
    MenuItem(
        "Template List",
        reverse("core-admin:core_main_app_templates"),
        icon="list",
    ),
    MenuItem(
        "Upload New Template",
        reverse("core-admin:core_main_app_upload_template"),
        icon="upload",
    ),
    MenuItem(
        "Data Migration",
        reverse("core-admin:core_main_app_data_migration"),
        icon="exchange-alt",
    ),
)

Menu.add_item(
    "admin", MenuItem("TEMPLATES", None, children=templates_children)
)

xslt_children = (
    MenuItem(
        "XSLT List", reverse("core-admin:core_main_app_xslt"), icon="list"
    ),
    MenuItem(
        "Upload New XSLT",
        reverse("core-admin:core_main_app_upload_xslt"),
        icon="upload",
    ),
)

Menu.add_item("admin", MenuItem("XSLT", None, children=xslt_children))
