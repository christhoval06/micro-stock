from django.contrib.auth.models import AbstractUser

from apps.company.models import WithCompany
from apps.utils import models as utils_models


class User(AbstractUser, WithCompany, utils_models.WithTimeStamp):
    class Meta(AbstractUser.Meta):
        permissions = [('can_generate_password', 'Can generate password'),
                       ('can_view_users', 'Can view users'),
                       ('can_change_password', 'Can change password')]

    def has_any_perms(self, *perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return any(self.has_perm(perm, obj) for perm in perm_list)
