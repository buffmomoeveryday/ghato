from django import template
import warnings

register = template.Library()


@register.filter(is_safe=False)
def length_is(value, arg):
    """Return a boolean of whether the value's length is the argument."""
 
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return ""
