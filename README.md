# core_main_app

core_main_app is a Django app.

# Quick start

1. Add "core_main_app" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
    ...
    "core_main_app",
]
```

2. Include the core_main_app URLconf in your project urls.py like this::

```python
url(r'^', include("core_main_app.urls")),
```