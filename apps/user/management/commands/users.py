from django.apps import apps
from django.core.management.base import BaseCommand

from apps.user.constants import GROUPS


class Command(BaseCommand):
    help = 'Populate db with default objects'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('--groups')
        parser.add_argument('--permissions')

    def handle(self, *args, **options):

        if options['groups']:
            for role in GROUPS:
                group_model = apps.get_model('auth', 'Group')
                # permissions = get_permitions(PERMISSIONS_BY_ROLES[role])
                new_group, created = group_model.objects.get_or_create(name=role)
                # new_group.permissions.add(*permissions)
                new_group.save()
                self.stdout.write(self.style.SUCCESS('Permission "%s" was created success!' % new_group.name))

        if options['permissions']:
            pass
            # create_permitions(self)
