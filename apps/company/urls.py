from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateCompanyView.as_view(), name='company_create'),
    path('department/create', views.CreateDepartmentView.as_view(), name='department_create'),
]
