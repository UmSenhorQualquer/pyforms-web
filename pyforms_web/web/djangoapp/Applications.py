import datetime, json, dill, os
from pysettings import conf
from crequest.middleware import CrequestMiddleware
from pyforms_web.web.djangoapp.middleware import PyFormsMiddleware

class ApplicationsLoader:

	_storage 	 = {}
	
	@staticmethod
	def register_instance(request, modulename, app_data=None):
		# check if the module was already imported, if not import it.
		if modulename not in ApplicationsLoader._storage:
			modules = modulename.split('.')
			moduleclass = __import__( '.'.join(modules[:-1]) , fromlist=[modules[-1]] )
			ApplicationsLoader._storage[modulename] = getattr(moduleclass, modules[-1])
		moduleclass = ApplicationsLoader._storage[modulename]
		app 		= moduleclass()

		data = [{'uid': app.uid, 'layout_position': 0, 'title':app.title}]
		for m in request.updated_apps.applications: m.commit()
		
		return data


	@staticmethod
	def remove_instance(request, application_id):
		if os.path.isfile('/var/www/orquestra-server/oppened-apps.dat'):
			with open('/var/www/orquestra-server/oppened-apps.dat', 'r') as f:
				ApplicationsLoader._opened_apps = dill.load(f)
		else:
			ApplicationsLoader._opened_apps = {}

		user_apps = ApplicationsLoader._opened_apps.get(request.user, None)
		if user_apps is None: return None
		user_apps.remove_app(application_id)

		with open('/var/www/orquestra-server/oppened-apps.dat', 'w') as f:
			dill.dump(ApplicationsLoader._opened_apps, f)
		
	@staticmethod
	def get_instance(request, application_id, app_data=None):
		app = PyFormsMiddleware.get_instance(application_id)
		if app is None: return None
		
		if app_data is not None: app.load_serialized_form(app_data)

		for m in request.updated_apps.applications: m.commit()
		
		return app


	@staticmethod
	def update_instance(request, application_id, app_data=None):
		app = PyFormsMiddleware.get_instance(application_id)
		if app is None: return None
		
		if app_data is not None: app.load_serialized_form(app_data)

		data = [r.serialize_form() for r in request.updated_apps.applications if r.is_new_app]
		
		for m in request.updated_apps.applications: m.commit()
		
		return data
