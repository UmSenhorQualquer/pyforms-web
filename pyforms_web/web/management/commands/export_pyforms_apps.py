from django.core.management.base import BaseCommand
from django.apps import apps
import os


class Command(BaseCommand):
    help = 'Configure generic expenses codes for each Group'

    def add_arguments(self, parser):
        parser.add_argument('appname', type=str)
        parser.add_argument('--model', type=str)


    def handle(self, *args, **options):
        appname  = options.get('appname')
        appmodel = options.get('model', None)
        
        # create the app folder
        apps_folder = '{0}_apps'.format(appname)
        if not os.path.exists(apps_folder):
            os.makedirs(apps_folder)

            # check if the __init__ file exists, if not created it.
            init_filepath = os.path.join(apps_folder, '__init__.py')
            if not os.path.exists(init_filepath):
                open(init_filepath, 'w').close()

        # check if the apps folder exists, if not create it.
        apps_folder = os.path.join(apps_folder, 'apps')
        if not os.path.exists(apps_folder): os.makedirs(apps_folder)

        # load app template
        template = os.path.join( os.path.dirname(__file__), '..','pyforms_app_template.py')
        template = bpod_settings = open(template, 'r').read()

        init_text = ''
        main_app = None

        if appmodel:
            # if the model is defined in the parameters, generate the file only for that model.
            models = [apps.get_model(appname, appmodel)]
        else:
            # generate the file for all the models.
            app    = apps.get_app_config(appname)
            models = app.get_models()

        for i, model in enumerate(models):
            if main_app is None: main_app = '>{0}AdminApp'.format(model.__name__)

            # app path
            apppath = os.path.join(apps_folder, '{0}_app.py'.format(model.__name__.lower()))
            
            # check if the app file exists.
            # if so, confirm if the file should be replaced.
            if os.path.exists(apppath):
                print()
                answer = ""
                while answer not in ["y", "n"]:
                    answer = input("The file [{0}] exists, do you want to replace it [Y/N]? ".format(apppath)).lower()
                if answer != "y": 
                    print()
                    print('The generation of the app [{0}AdminApp] was canceled.'.format(model.__name__))
                    print()
                    continue

            init_text  += 'from .{0}_app import {1}AdminApp\n'.format(model.__name__.lower(), model.__name__)
            
            fields_list = ["'"+field.name+"'" for field in model._meta.get_fields()]

            app_text = template.format(
                application_name=appname,
                model_name=model.__name__,
                model_verbose_name=model._meta.verbose_name_plural.title(),
                main_app=main_app if i>0 else '',
                order=i,
                fields_list=','.join(fields_list)
            )

            with open(apppath, 'w') as outfile:
                outfile.write(app_text)

        if init_text:
            init_path = os.path.join(apps_folder, '__init__.py')
            if os.path.exists(init_path):
                print('The __init__.py file exists, and it will not be replaced')
                print('Please add the next code manually to it.')
                print()
                print(init_text)
            else:
                with open(init_path, 'w') as outfile:
                    outfile.write(init_text)





            