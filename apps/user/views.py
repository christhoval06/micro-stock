import six
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView

from apps.utils.views.list import ListView
from apps.utils.views.with_email import WithEmailMixin
from .forms import UserCreateForm, UserUpdateForm, GeneratePasswordForm
from .models import User


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('user.add_user', 'home:index'), name='dispatch')
class UserCreateView(WithEmailMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:index')
    form_data = None

    email_html_template = "emails/welcome.html"
    email_subject_template = "emails/welcome_subject.txt"
    email_template = "emails/welcome.txt"

    def get_context_data(self, **kwargs):
        kwargs.update({
            'title': _('User Creation'),
            'save_message': _('Save New user')
        })
        return super().get_context_data(**kwargs)

    def get_email_context_data(self, **kwargs):
        kwargs.update({
            'created_user': self.object,
            'form_data': self.form_data,
            'message': _('Welcome'),
            'action_url': reverse_lazy('authentication: login'),
            'action_text': _('Sign In')
        })
        return super().get_email_context_data(**kwargs)

    def form_valid(self, form):
        r = super().form_valid(form)
        self.form_data = form.cleaned_data
        self.send_email(to=self.object.email)
        return r


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('user.change_user', 'home:index'), name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:index')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'title': _('User Update'),
            'save_message': _('Update current user')
        })
        return super().get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('user.can_generate_password', 'home:index'), name='dispatch')
class UserGeneratePasswordView(WithEmailMixin, UpdateView):
    form_class = GeneratePasswordForm
    template_name = 'user/generate_password.html'
    success_url = reverse_lazy('user:index')
    form_data = None
    model = User

    email_html_template = "emails/generate_password.html"
    email_subject_template = "emails/generate_password_subject.txt"
    email_template = "emails/generate_password.txt"

    def get_context_data(self, **kwargs):
        kwargs.update({
            'title': _('Password Generate'),
            'save_message': _('Do wish you generate a new password to this user?')
        })
        return super().get_context_data(**kwargs)

    def get_email_context_data(self, **kwargs):
        kwargs.update({
            'created_user': self.object,
            'form_data': self.form_data,
            'message': _('Password Generated'),
            'action_url': reverse_lazy('authentication:login'),
            'action_text': _('Sign In'),
        })
        return super().get_email_context_data(**kwargs)

    def form_valid(self, form):
        r = super().form_valid(form)
        self.form_data = form.cleaned_data
        self.send_email(to=self.object.email)
        return r


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('user.can_view_users', 'home:index'), name='dispatch')
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
        if not self.request.user.has_any_perms('user.can_generate_password', 'user.change_user'):
            return ''
        return mark_safe('''
        <span class="dropdown">
            <a href="#" class="btn m-btn m-btn--hover-brand m-btn--icon m-btn--icon-only m-btn--pill" data-toggle="dropdown" aria-expanded="true">
                <i class="la la-ellipsis-h"></i>
            </a>
            <div class="dropdown-menu dropdown-menu-right">
                {}
            </div>
        </span>'''.format(
            *list(map(lambda e: e[1] if e[0](self.request) else '',
                      [
                          (
                              lambda req: req.user.has_perm('user.change_user'),
                              '<a class="dropdown-item" href="{}"><i class="la la-edit"></i> {}</a>'.format(
                                  reverse_lazy('user:edit', kwargs={'pk': user.pk}),
                                  _('Edit Details')
                              )
                          ),
                          (
                              lambda req: req.user.has_perm('user.can_generate_password'),
                              '<a class="dropdown-item" href="{}"><i class="la la-print"></i> {}</a>'.format(
                                  reverse_lazy('user:generate_password', kwargs={'pk': user.pk}),
                                  _('Generate Password')
                              )
                          )
                      ]))
        ))

    actions.short_description = _('Actions')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'title': _('Users'),
            'alert': False,
            'alert_text': mark_safe('''Each column has an optional rendering control called columns.
             render which can be used to process the content of each cell before the data is used. 
             See official documentation <a href="{}" target="_blank">here</a>.'''.format('#')),
            'alert_icon': 'flaticon-exclamation',
            'add_visible': self.request.user.has_perm('user.add_user'),
            'add_title': _('Add User'),
            'add_url': 'user:create'
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
