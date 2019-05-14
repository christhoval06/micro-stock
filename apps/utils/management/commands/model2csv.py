import csv
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Output the specified model as CSV"

    def add_arguments(self, parser):
        parser.add_argument('appname.ModelName', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        from django.apps import apps
        app_name_model = kwargs.get('appname.ModelName')
        if app_name_model is None:
            return
        app_name, model_name = app_name_model[0].split('.')
        model = apps.get_model(app_name, model_name)
        field_names = [f.name for f in model._meta.fields][1:]
        writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
        writer.writerow(field_names)
        for instance in model.objects.all():
            writer.writerow([getattr(instance, f) for f in field_names])
