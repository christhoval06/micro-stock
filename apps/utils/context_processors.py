import sys
from functools import reduce

this = sys.modules[__name__]

MENU_FUNCS = ['_home', '_users', '_departments', '_products', '_customers', '_suppliers', '_stock', '_recipes',
              '_reports', '_settings']


def _home(request):
    return [
        {
            'type': 'item',
            'name': 'home',
            'text': 'Dashboard',
            'icon': 'flaticon-line-graph',
            'badge': 2,
            'url': 'home'
        },
    ]


def _users(request):
    return [
        {
            'type': 'section',
            'text': 'Users',
        },
        {
            'type': 'submenu',
            'text': 'Users',
            'name': 'users',
            'icon': 'flaticon-users',
            'open': False,
            'sub_menu': [
                {
                    'type': 'parent',
                    'text': 'Users',
                },
                {
                    'type': 'item',
                    'text': 'Create',
                    'url': 'user_create',
                    'name': 'user_create',
                    'active': False,
                },
                {
                    'type': 'submenu',
                    'text': 'Sub Menu',
                    'url': 'home',
                    'name': 'state_colors',
                    'active': False,
                    'sub_menu': [
                        {
                            'type': 'item',
                            'text': 'State Colors',
                            'url': 'home',
                            'name': 'state_colors',
                            'active': False,
                        },
                    ]
                },
            ]
        },
    ]


def _departments(request):
    return [
        {
            'type': 'section',
            'text': 'Departments',
        },
    ]


def _products(request):
    return [
        {
            'type': 'section',
            'text': 'Products',
        },
    ]


def _stock(request):
    return [
        {
            'type': 'section',
            'text': 'Stock',
        },
    ]


def _recipes(request):
    return [
        {
            'type': 'section',
            'text': 'Recipes',
        },
    ]


def _customers(request):
    return [
        {
            'type': 'section',
            'text': 'Customers',
        },
    ]


def _suppliers(request):
    return [
        {
            'type': 'section',
            'text': 'Suppliers',
        },
    ]


def _reports(request):
    return [
        {
            'type': 'section',
            'text': 'Reports',
        },
    ]


def _settings(request):
    return [
        {
            'type': 'section',
            'text': 'Settings',
        },
    ]


def menu(request):
    return {
        'menu': list(reduce(lambda o, c: o + getattr(this, c)(request), MENU_FUNCS, []))
    }


def breadcrumbs(request):
    return {
        'subheader_title': 'Users',
        'breadcrumbs': [
            {
                'text': 'Users',
                'url': 'home',
            },
            {
                'text': 'Create',
            }
        ]
    }
