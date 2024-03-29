from django import template
from django.template.defaulttags import register

register = template.Library()

@register.filter
def aMill(value):
    return int(value)/1000000

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def split_decimal(value):
    new_val = value.split('.')[1]
    return new_val