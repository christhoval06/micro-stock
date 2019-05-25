from django.urls import path

from . import views

app_name = 'authentication'
urlpatterns = [
    path('login/', views.AuthLoginView.as_view(), name='login'),
    path('logout/', views.AuthLogoutView.as_view(), name='logout'),

]
