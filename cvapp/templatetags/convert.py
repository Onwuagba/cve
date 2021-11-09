from django import template

register = template.Library()

@register.filter
def aMill(value):
    return int(value)/1000000