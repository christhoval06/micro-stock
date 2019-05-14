from django.contrib.auth.views import LoginView


class AuthLoginView(LoginView):
    template_name = 'auth/login.html'

    def get_context_data(self, **kwargs):
        ctx = super(AuthLoginView, self).get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'title': 'Sign In',
            })
        return ctx
