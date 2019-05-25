from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx.update({
            'title': 'Dashboard',
            'subheader_title': 'Home',
            'breadcrumbs': [
                {
                    'text': 'Name',
                    'url': 'home:index',
                },
                {
                    'text': 'Current',
                }
            ]
        })
        return ctx
