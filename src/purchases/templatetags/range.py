from django import template

register = template.Library()


@register.filter(name="range")
def _range(value):
    """
    Returns a range object for use in a template.
    """
    return range(value)
