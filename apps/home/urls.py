from django.urls import path

from . import views

app_name = 'home'

menu = [
    {
        'type': 'item',
        'name': 'home',
        'text': 'Dashboard',
        'icon': 'flaticon-line-graph',
        'badge': 2,
        'url': 'home:index',
        'active': False
    },
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
]
