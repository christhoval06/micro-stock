from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from .forms import CreateUserForm


@method_decorator(login_required, name='dispatch')
class CreateUserView(FormView):
    form_class = CreateUserForm
    template_name = 'user/create.html'

    def get_context_data(self, **kwargs):
        ctx = super(CreateUserView, self).get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'title': 'User Create',
            })
        return ctx
