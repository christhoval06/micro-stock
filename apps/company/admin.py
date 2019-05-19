from django.contrib import admin

from . import models


class DepartmentInline(admin.StackedInline):
    model = models.Department
    extra = 0


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'is_active']
    list_display = ['name', 'is_active']
    ordering = ['name']
    inlines = (DepartmentInline,)


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'company', 'is_active']
    list_display = ['name', 'company', 'is_active']
    ordering = ['name', 'company']
