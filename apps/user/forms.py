from django.contrib.auth import forms as django_forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from apps.user.models import User
from apps.utils.helpers import password
from apps.utils.helpers.username import get_random_user


class PasswordChangeForm(django_forms.PasswordChangeForm):
    pass


class UserForm(ModelForm):
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
            'title': _('Company Settings'),
            'fields': ['company']
        },
        {
            'title': _('Client Settings'),
            'fields': ['groups']
        }
    ]

    required_fields = ['first_name', 'last_name', 'email', 'groups', 'company']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_required_fields()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'groups', 'company']

    def set_required_fields(self):
        for field in self.required_fields:
            self.fields[field].required = True


class UserCreateForm(UserForm):
    def save(self, commit=True):
        self.cleaned_data.update({'password': password.generator()})
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = get_random_user(**self.cleaned_data)
        user.is_active = True
        return super().save()


class UserUpdateForm(UserForm):
    pass


class GeneratePasswordForm(UserForm):
    layouts = []
    required_fields = []

    class Meta(UserForm.Meta):
        fields = []

    def save(self, commit=True):
        self.cleaned_data.update({'password': password.generator()})
        user = super().save(False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
