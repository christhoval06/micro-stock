from django.views.defaults import page_not_found, server_error


def handler404(request, *args, **kwargs):
    print('args', args, 'kwargs', kwargs)
    return page_not_found(request, args, template_name='errors/404.html')


def handler500(request, *args):
    print('args', args)
    return server_error(request, template_name='errors/404.html')
