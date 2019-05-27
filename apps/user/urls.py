from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('list/', views.UserListView.as_view(), name='index'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='edit'),
    path('generate_password/<int:pk>/', views.UserGeneratePasswordView.as_view(), name='generate_password'),
]
