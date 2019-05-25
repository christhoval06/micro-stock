import sys
from functools import reduce

from django.conf import settings

this = sys.modules[__name__]

MENU_FUNCS = ['_home', '_users', '_company', '_products', '_customers', '_suppliers', '_stock', '_recipes',
              '_reports', '_settings']


def _home(request):
    return [
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


def _users(request):
    return [
        {
            'type': 'section',
            'text': 'Users',
        },
        {
            'type': 'submenu',
            'text': 'Users',
            'name': 'user',
            'icon': 'flaticon-users',
            'open': False,
            'sub_menu': [
                {
                    'type': 'parent',
                    'text': 'Users',
                },
                {
                    'type': 'item',
                    'text': 'List',
                    'url': 'user:index',
                    'active': False,
                },
                {
                    'type': 'item',
                    'text': 'Create',
                    'url': 'user:create',
                    'active': False,
                },
                {
                    'type': 'submenu',
                    'text': 'Sub Menu',
                    'name': 'submenu',
                    'active': False,
                    'sub_menu': [
                        {
                            'type': 'item',
                            'text': 'State Colors',
                            'url': 'home:index',
                            'active': False,
                        },
                    ]
                },
            ]
        },
    ]


def _company(request):
    return [
        {
            'type': 'section',
            'text': 'Companies',
        },
        {
            'type': 'submenu',
            'text': 'Companies',
            'name': 'company',
            'icon': 'flaticon-truck',
            'open': False,
            'sub_menu': [
                {
                    'type': 'parent',
                    'text': 'Companies',
                },
                {
                    'type': 'item',
                    'text': 'List',
                    'url': 'company:index',
                    'active': False,
                },
                {
                    'type': 'item',
                    'text': 'Create',
                    'url': 'company:create',
                    'active': False,
                },
            ]
        },
        {
            'type': 'submenu',
            'text': 'Departments',
            'name': 'company:department',
            'icon': 'flaticon-squares-4',
            'open': False,
            'sub_menu': [
                {
                    'type': 'parent',
                    'text': 'Departments',
                },
                {
                    'type': 'item',
                    'text': 'List',
                    'url': 'company:department:index',
                    'active': False,
                },
                {
                    'type': 'item',
                    'text': 'Create',
                    'url': 'company:department:create',
                    'active': False,
                },
            ]
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


def _map_menu_item(request, item):
    if item['type'] in ['submenu']:
        item['open'] = request.resolver_match.namespace == item['name']
        item['sub_menu'] = list(_iterate_menu(request, item['sub_menu']))
    elif item['type'] in ['item']:
        item['active'] = request.resolver_match.view_name == item['url']
    return item


def _iterate_menu(request, items=None):
    if items is None:
        items = list(reduce(lambda o, c: o + getattr(this, c)(request), MENU_FUNCS, []))
    return list(map(lambda item: _map_menu_item(request, item), items))


def menu(request):
    return {
        'app_name': settings.APP_NAME,
        'menu': _iterate_menu(request),
        'show_header_menu_actions': False,
        'show_header_menu_reports': False,
        'show_header_menu_apps': False,
        'show_header_toolbar_search': False,
        'show_header_toolbar_notifications': False,
        'show_header_toolbar_quick_actions': False,
        'show_header_toolbar_sidebar': False,
        'show_quick_nav_bar': False,
        'show_profile_menu_sections': False,
        'show_footer_menu': False,
        'developer': settings.DEVELOPER_NAME,
        'developer_site': settings.DEVELOPER_SITE,
        'show_copyright': False,
        'show_extra_charts': False,
    }


def breadcrumbs(request):
    resolver = request.resolver_match
    print('resolver', resolver.__dict__)
    print('resolver.func', resolver.func.view_class.__dict__)
    print('url_name', resolver.url_name, resolver.view_name)

    _menu_ = _iterate_menu(request)
    _section_ = list(filter(lambda i: i['type'] == 'submenu' and i['open'], _menu_))[0]
    _item_ = list(filter(lambda i: i['type'] == 'item' and i['active'], _section_['sub_menu']))[0]

    print('_section_', _section_)
    print('_item_', _item_)
    return {
        'subheader_title': _section_['text'],
        'breadcrumbs': [
            {
                'text': _section_['text'],
                'url': '{}:index'.format(_section_['name']),
            },
            {
                'text': _item_['text'],
            }
        ]
    }
