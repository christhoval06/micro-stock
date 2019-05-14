from decimal import Decimal
from enum import Enum
from json import dumps

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet
from django.utils.encoding import force_text


def is_model(o):
    # for cls in [Service, Client, Company, Group]:
    #     if isinstance(o, cls):
    #         return True
    return False


class ComplexJSONEncoder(DjangoJSONEncoder):

    def default(self, o):
        if is_model(o):
            return o.pk
        if type(o) is list or isinstance(o, QuerySet):
            if is_model(o[0]):
                return [v.id for v in o]
            return o
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, Enum):
            return o.value

        if o.__class__.__module__ == 'django.utils.functional':
            return force_text(o)

        return super(ComplexJSONEncoder, self).default(o)


def serialize(data):
    return dumps(data, cls=ComplexJSONEncoder)
