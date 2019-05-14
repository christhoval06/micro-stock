import json as simplejson
from datetime import datetime

from django import template
from django.utils import formats, timezone
from django.utils.html import escape

from apps.utils.helpers.json import ComplexJSONEncoder

register = template.Library()


@register.simple_tag
def to_dict(json):
    return simplejson.loads(json)


@register.simple_tag
def dict_get_value(data, key, default=None):
    return data.get(key, default)


@register.simple_tag
def to_datetime(s, f='%Y-%m-%d'):
    return formats.localize(timezone.template_localtime(datetime.strptime(s, f).date()))


@register.filter
def to_json_attr(obj):
    return escape(simplejson.dumps(obj, cls=ComplexJSONEncoder))
