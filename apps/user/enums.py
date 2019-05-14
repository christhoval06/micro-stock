from enum import Enum

from .constants import *


class GroupsTypes(Enum):
    SU = SU
    ADMIN = ADMIN
    SELLER = SELLER
    VIEWER = VIEWER
    USER = USER
