from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils import models as utils_models


class Company(utils_models.WithTimeStamp, models.Model):
    name = models.CharField(
        _('Name'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this company should be use or not in app.'
        ),
    )

    def __str__(self):
        return self.name


class WithCompany(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True


class Department(WithCompany, utils_models.WithTimeStamp, models.Model):
    name = models.CharField(
        _('Name'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer.'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this department should be use or not in app.'
        ),
    )

    def __str__(self):
        return self.name
