"""Menu configuration
"""
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem


Menu.add_item(
    "main", MenuItem("Home", reverse("core_main_app_homepage"), icon="home", weight=-1000)
)

Menu.add_item(
    "admin", MenuItem("Dashboard", reverse("admin:core_main_app_admin_home"), icon="dashboard", weight=-10000)
)

templates_children = (
    MenuItem("Template List", reverse("admin:core_main_app_templates"), icon="list"),
    MenuItem("Upload New Template", reverse("admin:core_main_app_upload_template"), icon="upload"),
)

Menu.add_item(
    "admin", MenuItem("TEMPLATES", None, children=templates_children)
)

xslt_children = (
    MenuItem("XSLT List", reverse("admin:core_main_app_xslt"), icon="list"),
    MenuItem("Upload New XSLT", reverse("admin:core_main_app_upload_xslt"), icon="upload")
)

Menu.add_item(
    "admin", MenuItem("XSLT", None, children=xslt_children)
)

users_admin_children = (
    MenuItem("Users", reverse("admin:auth_user_changelist"), icon="address-book-o"),
    MenuItem("Groups", reverse("admin:auth_group_changelist"), icon="users"),
    MenuItem("Authentication", reverse("admin:index"), icon="lock"),
)

Menu.add_item(
    "admin", MenuItem("USERS", None, weight=-9000, children=users_admin_children)
)


