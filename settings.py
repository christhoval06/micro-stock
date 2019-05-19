# -*- coding: utf-8 -*-

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings

aldryn_addons.settings.load(locals())

# all django settings can be altered here

SECRET_KEY = 'x^w*wyhyh5%1$%l@=5wa^56_+omn)b!-m9*+=uy0!%@!%ej0gy'

AUTH_USER_MODEL = 'user.User'

LOGOUT_REDIRECT_URL = 'home'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = '/auth/login/'

INSTALLED_APPS.extend([
    # add your project specific apps here
    'widget_tweaks',
    'channels',

    # 'apps.chat',
    'apps.authentication',
    'apps.user',
    'apps.home',
    'apps.company',
])

APP_NAME = 'Micro Stock'

TEMPLATES[0]['OPTIONS']['context_processors'].extend([
    'apps.utils.context_processors.menu',
])

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

TIME_ZONE = 'America/Panama'

# https://tutorial-extensions.djangogirls.org/es/heroku/

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = "hi@appname.com"

# Channels Settings

ASGI_APPLICATION = "routing.application"

# https://beefree.io/templates/


# https://github.com/cyantarek/django-stock-management-system/tree/master/app

# https://github.com/melizalab/django-lab-inventory/blob/master/inventory/models.py

# http://www.chrisumbel.com/article/django_python_stored_procedures.aspx
