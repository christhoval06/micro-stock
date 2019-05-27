from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from . import models


class CompanyForm(ModelForm):
    layouts = [
        {
            'title': _('Company Details'),
            'fields': ['name']
        },
        {
            'title': _('Company Settings'),
            'fields': ['is_active']
        }
    ]

    required_fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_required_fields()

    class Meta:
        model = models.Company
        fields = ['name', 'is_active', ]

    def set_required_fields(self):
        for field in self.required_fields:
            self.fields[field].required = True


class CompanyCreateForm(CompanyForm):
    pass


class CreateDepartmentForm(ModelForm):
    layouts = [
        {
            'title': _('Department Details'),
            'fields': ['name']
        },
        {
            'title': _('Department Settings'),
            'fields': ['company', 'is_active']
        }
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_required_fields()

    class Meta:
        model = models.Department
        fields = ['name', 'company', 'is_active', ]

    def set_required_fields(self):
        for field in ['name', 'company']:
            self.fields[field].required = True
