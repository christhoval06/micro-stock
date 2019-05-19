from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

from apps.utils.views.with_email import WithEmailMixin
from .forms import CreateUserForm


@method_decorator(login_required, name='dispatch')
class CreateUserView(WithEmailMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('home')
    form_data = None

    email_html_template = "emails/welcome.html"
    email_subject_template = "emails/welcome_subject.txt"
    email_template = "emails/welcome.txt"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'title': _('User Creation'),
            })
        return ctx

    def get_email_context_data(self, **kwargs):
        kwargs.update({
            'created_user': self.object,
            'form_data': self.form_data,
            'message': _('Welcome')
        })
        return super().get_email_context_data(**kwargs)

    def form_valid(self, form):
        r = super().form_valid(form)
        self.form_data = form.cleaned_data
        self.send_email(to=self.object.email)
        return r
