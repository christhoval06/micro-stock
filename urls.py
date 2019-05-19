# -*- coding: utf-8 -*-
import aldryn_addons.urls
from aldryn_django.utils import i18n_patterns

from django.urls import path, include

handler400 = 'apps.utils.views.errors.handler404'
handler403 = 'apps.utils.views.errors.handler404'
handler404 = 'apps.utils.views.errors.handler404'
handler500 = 'apps.utils.views.errors.handler500'

url_platform = [
    path('', include('apps.home.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('user/', include('apps.user.urls')),
    path('company/', include('apps.company.urls'))
]

urlpatterns = [
                  # add your own patterns here
                  *url_platform,
              ] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
