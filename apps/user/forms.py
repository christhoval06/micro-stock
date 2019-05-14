from django.contrib.auth import forms as django_forms
from django.forms import ModelForm

from apps.user.models import User


class LoginForm(django_forms.AuthenticationForm):
    pass


class PasswordChangeForm(django_forms.PasswordChangeForm):
    pass


class CreateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'username', 'email', 'is_active', 'groups', ]
