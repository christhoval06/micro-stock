from django.db import models


class Home(models.Model):
    class Meta:
        permissions = [('can_view_dashboard', 'Can view dashboard')]
