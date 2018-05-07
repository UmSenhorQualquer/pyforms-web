from django.core.management.base import BaseCommand
from django.apps import apps
import os


class Command(BaseCommand):
    help = 'Configure generic expenses codes for each Group'

    def add_arguments(self, parser):
        parser.add_argument('appname', type=str)


    def handle(self, *args, **options):
        appname = options.get('appname')
        
        #create the app folder
        apps_folder = '{0}_apps'.format(appname)
        if not os.path.exists(apps_folder):
            os.makedirs(apps_folder)
            open(os.path.join(apps_folder, '__init__.py'), 'w').close()

        apps_folder = os.path.join(apps_folder, 'apps')
        if not os.path.exists(apps_folder):
            os.makedirs(apps_folder)

        # load app template
        template = os.path.join(os.path.dirname(__file__), 'pyforms_app_template.py')
        template = bpod_settings = open(template, 'r').read()

        init_text = ''
        app = apps.get_app_config(appname)
        main_app = None
        for i, model in enumerate(app.get_models()):
            if main_app is None: main_app = '>{0}AdminApp'.format(model.__name__)

            init_text += 'from {0}_apps.apps.{1}_app import {2}AdminApp\n'.format(appname, model.__name__.lower(), model.__name__)

            fields_list = ["'"+field.name+"'" for field in model._meta.get_fields()]

            app_text = template.format(
                application_name=appname,
                model_name=model.__name__,
                model_verbose_name=model._meta.verbose_name_plural.title(),
                main_app=main_app if i>0 else '',
                order=i,
                fields_list=','.join(fields_list)
            )

            app_path = os.path.join(apps_folder, '{0}_app.py'.format(model.__name__.lower()))
            with open(app_path, 'w') as outfile:
                outfile.write(app_text)

        init_path = os.path.join(apps_folder, '__init__.py')
        with open(init_path, 'w') as outfile:
            outfile.write(init_text)





            