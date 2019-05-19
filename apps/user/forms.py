from django.contrib.auth import forms as django_forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from apps.user.models import User
from apps.utils.helpers import password
from apps.utils.helpers.username import get_random_user


class PasswordChangeForm(django_forms.PasswordChangeForm):
    pass


class CreateUserForm(ModelForm):
    layouts = [
        {
            'title': _('User Details'),
            'fields': ['first_name', 'last_name']
        },
        {
            'title': _('Account Details'),
            'fields': ['email']
        },
        {
            'title': _('Client Settings'),
            'fields': ['groups']
        }
    ]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.set_fields_required()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'groups', ]

    def set_fields_required(self):
        for field in ['first_name', 'last_name', 'email', 'groups', ]:
            self.fields[field].required = True

    def save(self, commit=True):
        self.cleaned_data.update({'password': password.generator()})
        user = super(CreateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = get_random_user(**self.cleaned_data)
        user.is_active = True
        return super(CreateUserForm, self).save()
