from django.utils.translation import ugettext_lazy as _

SU = 1
ADMIN = 2
SELLER = 3
VIEWER = 4
USER = 5

SU_NAME = _('Su')
ADMIN_NAME = _('Admin')
SELLER_NAME = _('Seller')
VIEWER_NAME = _('Viewer')
USER_NAME = _('User')

GROUPS = [SU_NAME, ADMIN_NAME, SELLER_NAME, VIEWER_NAME, USER_NAME]
