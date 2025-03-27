# myapp/templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, class_name):
    return value.as_widget(attrs={'class': class_name})
