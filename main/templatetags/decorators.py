from django.template import Library
from rolepermissions import checkers

register = Library()

@register.simple_tag(name='has_role')
def has_role(user, role):
    return checkers.has_role(user, role)
