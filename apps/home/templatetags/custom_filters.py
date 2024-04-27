from django import template

register = template.Library()


@register.filter(name='starts_with')
def starts_with(value, arg):
    """
    Check if value starts with the specified argument.
    """
    return value.startswith(arg)


# Ensure that the filter is registered
register.filter('starts_with', starts_with)
