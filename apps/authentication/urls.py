from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.AuthLoginView.as_view(), name='auth_login'),
    path('logout/', views.AuthLogoutView.as_view(), name='auth_logout'),

]
