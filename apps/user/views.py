import six
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

from apps.utils.views.list import ListView
from apps.utils.views.with_email import WithEmailMixin
from .forms import CreateUserForm
from .models import User


@method_decorator(login_required, name='dispatch')
class UserCreateView(WithEmailMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:index')
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


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    list_display = ['name', 'email', 'status', 'created', 'actions']
    template_name = 'user/user_list.html'

    def name(self, user):
        states = ['success', 'brand', 'danger', 'accent', 'warning', 'metal', 'primary', 'info']
        return mark_safe('''<div class="m-card-user m-card-user--sm">
                                <div class="m-card-user__pic">
                                    <div class="m-card-user__no-photo m--bg-fill-{}"><span>{}</span></div>
                                </div>
                                <div class="m-card-user__details">
                                    <span class="m-card-user__name">{}</span>
                                    <a href="mailto:{}" class="m-card-user__email m-link">{}</a>
                                </div>
                            </div>'''.format('info', user.first_name[0], user.get_full_name(), user.email,
                                             user.email))

    name.short_description = _("Name")
    name.orderable = True
    name.visible = True

    def email(self, user):
        return user.email

    email.short_description = _('Email')
    email.orderable = True

    def status(self, user):
        status = {
            1: {'title': 'Pending', 'class': 'm-badge--brand'},
            2: {'title': 'Delivered', 'class': ' m-badge--metal'},
            3: {'title': 'Canceled', 'class': ' m-badge--primary'},
            4: {'title': 'Success', 'class': ' m-badge--success'},
            5: {'title': 'Info', 'class': ' m-badge--info'},
            6: {'title': 'Danger', 'class': ' m-badge--danger'},
            7: {'title': 'Warning', 'class': ' m-badge--warning'},
        }
        status_class = 'm-badge--success' if user.is_active else 'm-badge--danger'
        status = 'Active' if user.is_active else 'Inactive'
        return mark_safe('''<span class="m-badge {} m-badge--wide">{}</span>'''.format(status_class, status))

    status.short_description = _('Status')
    status.orderable = True

    def created(self, user):
        return user.created_at.strftime('%B %d %Y')

    created.short_description = _('Created')
    created.orderable = True

    def actions(self, user):
        return mark_safe('''
        <span class="dropdown">
            <a href="#" class="btn m-btn m-btn--hover-brand m-btn--icon m-btn--icon-only m-btn--pill" data-toggle="dropdown" aria-expanded="true">
                <i class="la la-ellipsis-h"></i>
            </a>
            <div class="dropdown-menu dropdown-menu-right">
                <a class="dropdown-item" href="#"><i class="la la-edit"></i> Edit Details</a>
                <a class="dropdown-item" href="#"><i class="la la-leaf"></i> Update Status</a>
                <a class="dropdown-item" href="#"><i class="la la-print"></i> Generate Report</a>
            </div>
        </span>
        <a href="#" class="m-portlet__nav-link btn m-btn m-btn--hover-brand m-btn--icon m-btn--icon-only m-btn--pill" title="View">
            <i class="la la-edit"></i>
        </a>''')

    actions.short_description = _('Actions')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'title': _('Users'),
            'alert': True,
            'alert_text': mark_safe('''Each column has an optional rendering control called columns.
             render which can be used to process the content of each cell before the data is used. 
             See official documentation <a href="{}" target="_blank">here</a>.'''.format('#')),
            'alert_icon': 'flaticon-exclamation'
        })
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = User.objects.all()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset
