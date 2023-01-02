import inspect
import logging
import traceback

import simplejson
from confapp import conf
from django.core.exceptions import PermissionDenied

from pyforms_web.web.middleware import PyFormsMiddleware

logger = logging.getLogger(__name__)

class ApplicationsLoader:
    _storage = {}

    @staticmethod
    def register_instance(request, modulename, app_data=None):

        if modulename in conf.PYFORMS_APPS:
            modulename = conf.PYFORMS_APPS[modulename]

        # check if the module was already imported, if not import it.
        if modulename not in ApplicationsLoader._storage:
            modules = str(modulename).split('.')
            moduleclass = __import__('.'.join(modules[:-1]), fromlist=[modules[-1]])
            ApplicationsLoader._storage[modulename] = getattr(moduleclass, modules[-1])
        moduleclass = ApplicationsLoader._storage[modulename]

        data = simplejson.loads(request.body)

        ## load the constructor parameters sent by the web client and init the app ###
        parameters = {}
        constructor_data = data.get('constructor', {})
        for name, param in inspect.signature(moduleclass).parameters.items():
            parameters[name] = constructor_data.get(name, None)

        app = moduleclass(**parameters)
        ###############################################################################

        ## load the method parameters sent by the web client and execute it ###########
        parameters = {}
        method_data = data.get('method', {})
        if 'method' in method_data:
            func = getattr(app, method_data['method'])
            for name, param in inspect.getargspec(func):
                parameters[name] = method_data.get(name, None)
            func(**parameters)
        ###############################################################################

        data = [{'uid': app.uid, 'layout_position': app.LAYOUT_POSITION, 'title': app.title} for app in request.updated_apps.applications if app.is_new_app]
        for m in request.updated_apps.applications: m.commit()

        return data

    @staticmethod
    def remove_instance(request, application_id):
        return PyFormsMiddleware.remove_instance(application_id)

    @staticmethod
    def get_instance(request, application_id, app_data=None):
        app = PyFormsMiddleware.get_instance(application_id)

        if app is None: return None

        if not app.has_session_permissions(request.user):
            raise PermissionDenied('The user does not have access to the application')

        if app_data is not None: app.deserialize_form(app_data)

        for m in request.updated_apps.applications: m.commit()

        return app

    @staticmethod
    def update_instance(request, application_id, app_data=None):
        app = PyFormsMiddleware.get_instance(application_id)
        if app is None: return None

        if app_data is not None:
            try:
                app.deserialize_form(app_data)
            except Exception as e:
                logger.critical(e, exc_info=True)
                app.alert(str(e))

        return ApplicationsLoader.get_data(request)

    @staticmethod
    def get_data(request):
        """
        Function called to collect the pyforms updates to be send to the client
        :param request: HttpRequest
        :return dict: Data to send to the client browser
        """
        data = [r.serialize_form() for r in request.updated_apps.applications]
        for m in request.updated_apps.applications: m.commit()

        return data
