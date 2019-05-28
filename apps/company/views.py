import six
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, UpdateView

from apps.utils.views.list import ListView
from .forms import CreateDepartmentForm, CompanyCreateForm
from .models import Company, Department


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('company.change_company', 'home:index'), name='dispatch')
class CompanyCreateView(CreateView):
    form_class = CompanyCreateForm
    template_name = 'company/create.html'
    success_url = reverse_lazy('company:index')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'title': _('Company Creation'),
            })
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('company.change_company', 'home:index'), name='dispatch')
class CompanyUpdateView(UpdateView):
    form_class = CompanyCreateForm
    template_name = 'company/create.html'
    success_url = reverse_lazy('company:index')
    model = Company

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'title': _('Company Update'),
            })
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('company.add_department', 'home:index'), name='dispatch')
class DepartmentCreateView(CreateView):
    form_class = CreateDepartmentForm
    template_name = 'company/create.html'
    success_url = reverse_lazy('company:department:index')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'title': _('Department Creation'),
            })
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('company.change_department', 'home:index'), name='dispatch')
class DepartmentUpdateView(UpdateView):
    form_class = CompanyCreateForm
    template_name = 'company/create.html'
    success_url = reverse_lazy('company:department:index')
    model = Department

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'title': _('Department Update'),
            })
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('company.can_view_companies', 'home:index'), name='dispatch')
class CompanyListView(ListView):
    list_display = ['name', 'status', 'created', 'actions']
    template_name = 'company/company_list.html'

    def name(self, company):
        state = 'brand'
        return mark_safe('''<div class="m-card-user m-card-user--sm">
                                <div class="m-card-user__pic">
                                    <div class="m-card-user__no-photo m--bg-fill-{}"><span>{}</span></div>
                                </div>
                                <div class="m-card-user__details">
                                    <span class="m-card-user__name">{}</span>
                                </div>
                            </div>'''.format(state, company.name[0], company.name))

    name.short_description = _("Name")
    name.orderable = True
    name.visible = True

    def status(self, company):
        status_class = 'm-badge--success' if company.is_active else 'm-badge--danger'
        status = 'Active' if company.is_active else 'Inactive'
        return mark_safe('''<span class="m-badge {} m-badge--wide">{}</span>'''.format(status_class, status))

    status.short_description = _('Status')
    status.orderable = True

    def created(self, company):
        return company.created_at.strftime('%B %d %Y')

    created.short_description = _('Created')
    created.orderable = True

    def actions(self, company):
        if not self.request.user.has_any_perms('company.add_company', 'company.add_department'):
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
                          # (
                          #     lambda req: req.user.has_perm('company.update_department'),
                          #     '<a class="dropdown-item" href="{}"><i class="la la-plus"></i> {}</a>'.format(
                          #         reverse_lazy('company:department:create', kwargs={'pk': company.pk}),
                          #         _('Add Department')
                          #     )
                          # ),
                          (
                              lambda req: req.user.has_perm('company.change_company'),
                              '<a class="dropdown-item" href="{}"><i class="la la-edit"></i> {}</a>'.format(
                                  reverse_lazy('company:edit', kwargs={'pk': company.pk}),
                                  _('Edit Details')
                              )
                          )
                      ]))
        ))

    actions.short_description = _('Actions')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'title': _('Companies'),
            'alert': False,
            'alert_text': mark_safe('''Each column has an optional rendering control called columns.
             render which can be used to process the content of each cell before the data is used. 
             See official documentation <a href="{}" target="_blank">here</a>.'''.format('#')),
            'alert_icon': 'flaticon-exclamation',
            'add_visible': self.request.user.has_perm('company.add_company'),
            'add_title': _('Add Company'),
            'add_url': 'company:create'
        })
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = Company.objects.all()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('company.can_view_departments', 'home:index'), name='dispatch')
class DepartmentListView(ListView):
    list_display = ['name', 'company', 'status', 'created', 'actions']
    template_name = 'company/company_list.html'

    def name(self, department):
        state = 'brand'
        return mark_safe('''<div class="m-card-user m-card-user--sm">
                                <div class="m-card-user__pic">
                                    <div class="m-card-user__no-photo m--bg-fill-{}"><span>{}</span></div>
                                </div>
                                <div class="m-card-user__details">
                                    <span class="m-card-user__name">{}</span>
                                </div>
                            </div>'''.format(state, department.name[0], department.name))

    name.short_description = _("Name")
    name.orderable = True
    name.visible = True

    def company(self, department):
        return department.company.name

    company.short_description = _('Status')
    company.orderable = True

    def status(self, department):
        status_class = 'm-badge--success' if department.is_active else 'm-badge--danger'
        status = 'Active' if department.is_active else 'Inactive'
        return mark_safe('''<span class="m-badge {} m-badge--wide">{}</span>'''.format(status_class, status))

    status.short_description = _('Status')
    status.orderable = True

    def created(self, department):
        return department.created_at.strftime('%B %d %Y')

    created.short_description = _('Created')
    created.orderable = True

    def actions(self, department):

        if not self.request.user.has_any_perms('company.change_department'):
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
                              lambda req: req.user.has_perm('company.change_department'),
                              '<a class="dropdown-item" href="{}"><i class="la la-edit"></i> {}</a>'.format(
                                  reverse_lazy('company:department:edit', kwargs={'pk': department.pk}),
                                  _('Edit Details')
                              )
                          )
                      ]))
        ))

    actions.short_description = _('Actions')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'title': _('Departments'),
            'alert': False,
            'alert_text': mark_safe('''Each column has an optional rendering control called columns.
             render which can be used to process the content of each cell before the data is used. 
             See official documentation <a href="{}" target="_blank">here</a>.'''.format('#')),
            'alert_icon': 'flaticon-exclamation',
            'add_visible': self.request.user.has_perm('company.add_department'),
            'add_title': _('Add Department'),
            'add_url': 'company:department:create'
        })
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = Department.objects.all()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset
