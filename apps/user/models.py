from django.contrib.auth.models import AbstractUser

from apps.company.models import WithCompany
from apps.utils import models as utils_models


class User(AbstractUser, WithCompany, utils_models.WithTimeStamp):
    pass
