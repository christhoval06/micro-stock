from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url


def user_passes_test(auth_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if auth_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator


def login_required(f=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """

    user_model = get_user_model()
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        # lambda u: user_model.objects.get(pk=u.id).first_time_terms is False,
        # lambda u: user_model.objects.get(pk=u.id).first_time_password is False,
        # lambda u: user_model.objects.get(pk=u.id).securityresponse_set.all() and user_model.objects.get(pk=u.id).securityresponse_set.all().count() >= 3,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if f:
        return actual_decorator(f)
    return actual_decorator
