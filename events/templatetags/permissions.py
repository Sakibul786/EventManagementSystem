from django import template

register = template.Library()


@register.filter
def has_group(user, group_name):
    """
    Usage:
    {% if user|has_group:"Admin" %}
    """

    return user.groups.filter(name=group_name).exists()