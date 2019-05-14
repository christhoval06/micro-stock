from django import template
from django.apps import apps

from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    if user.is_superuser:
        return True
    try:
        group_model = apps.get_model('django.contrib.auth', 'Group')
        group = group_model.objects.get(name=group_name)
        return group in user.groups.all()
    except ObjectDoesNotExist:
        return False
