from datetime import datetime

from django import template

register = template.Library()


@register.filter(name='field_type')
def field_type(field):
    return field.field.widget.__class__.__name__


@register.filter(name='in_type')
def in_type(field, types):
    name = field.field.widget.__class__.__name__
    types = types.split(',')
    return name in types


# simple_tag: Processes the data and returns a string
# inclusion_tag: Processes the data and returns a rendered template
# assignment_tag: Processes the data and sets a variable in the context


@register.simple_tag
def current_time(format_string):
    return datetime.now().strftime(format_string)


@register.simple_tag
def define(val=None):
    return val


@register.simple_tag
def class_name(klass):
    return klass.__class__.__name__
