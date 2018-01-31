from django import template

register = template.Library()

@register.filter(name='ifinlist')
def ifinlist(value, list):
    for listItem in list:
        if value.pk == listItem.pk:
            return True
    return False