from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template import loader

from django.views.generic import View


class WithEmailMixin(View):
    email_html_template = "emails/generic.html"
    email_template = 'emails/generic.txt'
    email_subject_template = 'emails/generic_subject.txt'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = None

        self.user = get_object_or_404(get_user_model(), pk=self.request.user.pk)
        return super(WithEmailMixin, self).dispatch(request, *args, **kwargs)

    def _get_site(self):
        return get_current_site(self.request)

    def get_email_context_data(self, **kwargs):
        return kwargs

    def send_email(self, to=None):
        context = {
            'site': self._get_site(),
            'user': self.user,
            'username': self.user.get_username(),
            'secure': self.request.is_secure(),
            'domain': "http{}://{}".format('s' if self.request.is_secure() else '', self._get_site().domain),
            'app_name': settings.APP_NAME,
            **self.get_email_context_data()
        }
        body = loader.render_to_string(self.email_template, context).strip()
        html_message = loader.render_to_string(self.email_html_template, context).strip()
        subject = loader.render_to_string(self.email_subject_template, context).strip()
        r = send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to or self.user.email], html_message=html_message)
