from django.urls import path, include

from . import views

app_name = 'company'

department_patterns = ([
                           path('list/', views.DepartmentListView.as_view(), name='index'),
                           path('create/', views.DepartmentCreateView.as_view(), name='create'),
                           path('<int:pk>/', views.DepartmentCreateView.as_view(), name='detail'),
                       ], 'department')

urlpatterns = [
    path('create/', views.CompanyCreateView.as_view(), name='create'),
    path('list/', views.CompanyListView.as_view(), name='index'),

    path('department/', include(department_patterns)),

]
