from django import template

register = template.Library()


@register.filter(name="get_attribute")
def get_attribute(value, arg):
    """@see https://stackoverflow.com/questions/844746/performing-a-getattr-style-lookup-in-a-django-template"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif isinstance(value, dict) and arg in value:
        return value[arg]
    elif arg.isdigit() and len(value) > int(arg):
        return value[int(arg)]
    else:
        return ""
