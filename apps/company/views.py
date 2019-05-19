from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

from .forms import CreateDepartmentForm, CreateCompanyForm


@method_decorator(login_required, name='dispatch')
class CreateCompanyView(CreateView):
    form_class = CreateCompanyForm
    template_name = 'company/create.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'title': _('Company Creation'),
            })
        return ctx


@method_decorator(login_required, name='dispatch')
class CreateDepartmentView(CreateView):
    form_class = CreateDepartmentForm
    template_name = 'company/create.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'title': _('Department Creation'),
            })
        return ctx
