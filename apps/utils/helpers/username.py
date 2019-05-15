from random import randint

from django.apps import apps

from apps.utils.helpers.string import strip_accents


def get_random_user(**kwargs):
    user_model = apps.get_model('user', 'User')
    first_name = kwargs.get('first_name')
    last_name = kwargs.get('last_name')
    username = generate_default_username(first_name, last_name, is_random=kwargs.get('is_random', False))
    if user_model.objects.filter(username=username).exists():
        return get_random_user(**{**kwargs, 'is_random': True})
    return username


def generate_default_username(first_name, last_name, is_random=False):
    return strip_accents(
        ''.join([
            first_name.strip(),
            last_name.strip()[0],
            str(randint(1, 1000)) if is_random else ''
        ]).lower())
