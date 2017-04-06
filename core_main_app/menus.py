from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

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
    MenuItem("Users", reverse("admin:core_main_app_templates"), icon="address-book-o"),
    MenuItem("Groups", reverse("admin:core_main_app_templates"), icon="users"),
    MenuItem("Authentication", reverse("admin:core_main_app_templates"), icon="lock"),
)

Menu.add_item(
    "admin", MenuItem("USERS", None, weight=-9000, children=users_admin_children)
)


