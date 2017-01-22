import datetime, json, dill, os
from pysettings import conf
from crequest.middleware import CrequestMiddleware



class ApplicationsLoader:

	_storage = {}
	_opened_apps = {}

	@staticmethod
	def createInstance(modulename):

		if modulename not in ApplicationsLoader._storage:
			modules = modulename.split('.')
			moduleclass = __import__( '.'.join(modules[:-1]) , fromlist=[modules[-1]] )
			ApplicationsLoader._storage[modulename] = getattr(moduleclass, modules[-1])
		
		moduleclass = ApplicationsLoader._storage[modulename]

		obj = moduleclass()
		#obj.modulename = modulename
		return obj

	@staticmethod
	def create_instance(request, modulename, app_data=None):
		if os.path.isfile('/var/www/orquestra-server/oppened-apps.dat'):
			with open('/var/www/orquestra-server/oppened-apps.dat', 'r') as f:
				ApplicationsLoader._opened_apps = dill.load(f)
		else:
			ApplicationsLoader._opened_apps = {}

		updated_apps = request.updated_apps = Apps2Update()

		# check if the module was already imported, if not import it.
		if modulename not in ApplicationsLoader._storage:
			modules = modulename.split('.')
			moduleclass = __import__( '.'.join(modules[:-1]) , fromlist=[modules[-1]] )
			ApplicationsLoader._storage[modulename] = getattr(moduleclass, modules[-1])
		
		moduleclass = ApplicationsLoader._storage[modulename]
		app = moduleclass()

		for m in updated_apps.applications: m.commit()

		with open('/var/www/orquestra-server/oppened-apps.dat', 'w') as f:
			dill.dump(ApplicationsLoader._opened_apps, f)
		

		return app

	@staticmethod
	def run_instance(request, modulename, app_data=None):
		if os.path.isfile('/var/www/orquestra-server/oppened-apps.dat'):
			with open('/var/www/orquestra-server/oppened-apps.dat', 'r') as f:
				ApplicationsLoader._opened_apps = dill.load(f)
		else:
			ApplicationsLoader._opened_apps = {}

		updated_apps = request.updated_apps = Apps2Update()

		# check if the module was already imported, if not import it.
		if modulename not in ApplicationsLoader._storage:
			modules = modulename.split('.')
			moduleclass = __import__( '.'.join(modules[:-1]) , fromlist=[modules[-1]] )
			ApplicationsLoader._storage[modulename] = getattr(moduleclass, modules[-1])
		
		moduleclass = ApplicationsLoader._storage[modulename]
		app = moduleclass()

		results = updated_apps.applications
		data = [r.serializeForm() for r in results if r.is_new_app]
		for m in results: m.commit()

		with open('/var/www/orquestra-server/oppened-apps.dat', 'w') as f:
			dill.dump(ApplicationsLoader._opened_apps, f)

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
		if os.path.isfile('/var/www/orquestra-server/oppened-apps.dat'):
			with open('/var/www/orquestra-server/oppened-apps.dat', 'r') as f:
				ApplicationsLoader._opened_apps = dill.load(f)
		else:
			ApplicationsLoader._opened_apps = {}

		updated_apps = request.updated_apps = Apps2Update()

		user_apps = ApplicationsLoader._opened_apps.get(request.user, None)
		if user_apps is None: return None
		app = user_apps.get_app(application_id)
		if app is None: return None

		if app_data is not None: app.loadSerializedForm(app_data)

		for m in updated_apps.applications: m.commit()

		with open('/var/www/orquestra-server/oppened-apps.dat', 'w') as f:
			dill.dump(ApplicationsLoader._opened_apps, f)
		return app


	@staticmethod
	def update_instance(request, application_id, app_data=None):
		if os.path.isfile('/var/www/orquestra-server/oppened-apps.dat'):
			with open('/var/www/orquestra-server/oppened-apps.dat', 'r') as f:
				ApplicationsLoader._opened_apps = dill.load(f)
		else:
			ApplicationsLoader._opened_apps = {}

		updated_apps = request.updated_apps = Apps2Update()

		user_apps = ApplicationsLoader._opened_apps.get(request.user, None)
		if user_apps is None: return None
		app = user_apps.get_app(application_id)
		if app is None: return None
		if app_data is not None: app.loadSerializedForm(app_data)

		results = updated_apps.applications
		data = [r.serializeForm() for r in results if r.is_new_app]
		for m in results: m.commit()

		with open('/var/www/orquestra-server/oppened-apps.dat', 'w') as f:
			dill.dump(ApplicationsLoader._opened_apps, f)

		return data
	"""
	@staticmethod
	def createInstance(modulename, user, data=None, app_id=None ):
		if os.path.isfile('/var/www/orquestra-server/oppened-apps.dat'):
			with open('/var/www/orquestra-server/oppened-apps.dat', 'r') as f:
				ApplicationsLoader._opened_apps = dill.load(f)
		else:
			ApplicationsLoader._opened_apps = {}

		if data is not None or app_id is not None:
			if app_id is None: app_id = data['uid']
			app  = ApplicationsLoader._opened_apps[user].get_app(app_id)
		else:
			if modulename not in ApplicationsLoader._storage:
				modules = modulename.split('.')
				moduleclass = __import__( '.'.join(modules[:-1]) , fromlist=[modules[-1]] )
				ApplicationsLoader._storage[modulename] = getattr(moduleclass, modules[-1])
			
			moduleclass = ApplicationsLoader._storage[modulename]

			app = moduleclass()
			app.application = modulename

		with open('/var/www/orquestra-server/oppened-apps.dat', 'w') as f:
			dill.dump(ApplicationsLoader._opened_apps, f)
			
		return app"""

	@staticmethod
	def add_app(user, app):
		if os.path.isfile('/var/www/orquestra-server/oppened-apps.dat'):
			with open('/var/www/orquestra-server/oppened-apps.dat', 'r') as f:
				ApplicationsLoader._opened_apps = dill.load(f)
		else:
			ApplicationsLoader._opened_apps = {}

		# register the application globaly
		if user not in ApplicationsLoader._opened_apps.keys():
			ApplicationsLoader._opened_apps[user] = UserRunningApps()
		ApplicationsLoader._opened_apps[user].add_app(app)
		CrequestMiddleware.get_request().updated_apps.add_top(app)

		with open('/var/www/orquestra-server/oppened-apps.dat', 'w') as f:
			dill.dump(ApplicationsLoader._opened_apps, f)
		
	