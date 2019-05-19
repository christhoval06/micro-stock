from django.contrib import admin

from . import models


@admin.register(models.User)
class ClientAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_display = ['username', 'first_name', 'last_name', 'company', 'date_joined']
    ordering = ['username', 'company']
