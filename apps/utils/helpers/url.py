from django.urls import resolve


def enabled_url(request, *args):
    return resolve(request.path_info).url_name in args
