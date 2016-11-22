import datetime, json, dill, os
from pysettings import conf
from crequest.middleware import CrequestMiddleware

class Apps2Update(object):

	def __init__(self):
		self._top_apps = []
		self._bottom_apps = []

	def add_top(self, app):
		if app in self._bottom_apps: return
		if app in self._top_apps: return

		self._top_apps.append(app)

	def add_bottom(self, app):
		if app in self._top_apps: self._top_apps.remove(app)
		if app in self._bottom_apps: return
		
		self._bottom_apps.append(app)

	@property
	def applications(self): return self._top_apps+self._bottom_apps

class UserRunningApps(object):

	def __init__(self):
		self._apps = {}

	def add_app(self, app):
		if app.uid in self._apps.keys(): return
		self._apps[app.uid] = [datetime.datetime.now(), app]

		
	def remove_app(self, app_id):
		item = self._apps.get(app_id, None)
		if item is not None: del self._apps[app_id]

	def get_app(self, app_id): 
		#self.__garbage_collector()
		
		item = self._apps.get(app_id, None)

		if item is not None:
			item[0] = datetime.datetime.now()
			return item[1]
		else:
			return None

	def __garbage_collector(self):
		now = datetime.datetime.now()
		keys_2_del = []
		for key, [last_update, app] in self._apps.items():
			diff = now-last_update
			if diff.total_seconds()>conf.PYFORMS_WEB_APPLICATION_TIMEOUT: keys_2_del.append(key)

		for key in keys_2_del: del self._apps[key]


class ApplicationsLoader:

	_storage = {}
	_opened_apps = {}

	@staticmethod
	def create_instance(request, modulename, app_data=None):
		if os.path.isfile('oppened-apps.dat'):
			with open('oppened-apps.dat', 'r') as f:
				self._opened_apps = dill.loads(f)
		else:
			self._opened_apps = {}
		
		updated_apps = request.updated_apps = Apps2Update()

		# check if the module was already imported, if not import it.
		if modulename not in ApplicationsLoader._storage:
			modules = modulename.split('.')
			moduleclass = __import__( '.'.join(modules[:-1]) , fromlist=[modules[-1]] )
			ApplicationsLoader._storage[modulename] = getattr(moduleclass, modules[-1])
		
		moduleclass = ApplicationsLoader._storage[modulename]
		app = moduleclass()

		for m in updated_apps.applications: m.commit()

		with open('oppened-apps.dat', 'w') as f:
			dill.dump(self._opened_apps, f)
		

		return app

	@staticmethod
	def run_instance(request, modulename, app_data=None):
		if os.path.isfile('oppened-apps.dat'):
			with open('oppened-apps.dat', 'r') as f:
				self._opened_apps = dill.loads(f)
		else:
			self._opened_apps = {}

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

		with open('oppened-apps.dat', 'w') as f:
			dill.dump(self._opened_apps, f)

		return data

	@staticmethod
	def remove_instance(request, application_id):
		if os.path.isfile('oppened-apps.dat'):
			with open('oppened-apps.dat', 'r') as f:
				self._opened_apps = dill.loads(f)
		else:
			self._opened_apps = {}

		user_apps = ApplicationsLoader._opened_apps.get(request.user, None)
		if user_apps is None: return None
		user_apps.remove_app(application_id)

		with open('oppened-apps.dat', 'w') as f:
			dill.dump(self._opened_apps, f)
		
	@staticmethod
	def get_instance(request, application_id, app_data=None):
		if os.path.isfile('oppened-apps.dat'):
			with open('oppened-apps.dat', 'r') as f:
				self._opened_apps = dill.loads(f)
		else:
			self._opened_apps = {}

		updated_apps = request.updated_apps = Apps2Update()

		user_apps = ApplicationsLoader._opened_apps.get(request.user, None)
		if user_apps is None: return None
		app = user_apps.get_app(application_id)
		if app is None: return None

		if app_data is not None: app.loadSerializedForm(app_data)

		for m in updated_apps.applications: m.commit()

		with open('oppened-apps.dat', 'w') as f:
			dill.dump(self._opened_apps, f)
		return app


	@staticmethod
	def update_instance(request, application_id, app_data=None):
		if os.path.isfile('oppened-apps.dat'):
			with open('oppened-apps.dat', 'r') as f:
				self._opened_apps = dill.loads(f)
		else:
			self._opened_apps = {}

		updated_apps = request.updated_apps = Apps2Update()

		user_apps = ApplicationsLoader._opened_apps.get(request.user, None)
		if user_apps is None: return None
		app = user_apps.get_app(application_id)
		if app is None: return None
		if app_data is not None: app.loadSerializedForm(app_data)

		results = updated_apps.applications
		data = [r.serializeForm() for r in results if r.is_new_app]
		for m in results: m.commit()

		with open('oppened-apps.dat', 'w') as f:
			dill.dump(self._opened_apps, f)

		return data

	@staticmethod
	def createInstance(modulename, user, data=None, app_id=None ):
		if os.path.isfile('oppened-apps.dat'):
			with open('oppened-apps.dat', 'r') as f:
				self._opened_apps = dill.loads(f)
		else:
			self._opened_apps = {}

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

		with open('oppened-apps.dat', 'w') as f:
			dill.dump(self._opened_apps, f)
			
		return app

	@staticmethod
	def add_app(user, app):
		if os.path.isfile('oppened-apps.dat'):
			with open('oppened-apps.dat', 'r') as f:
				self._opened_apps = dill.loads(f)
		else:
			self._opened_apps = {}

		# register the application globaly
		if user not in ApplicationsLoader._opened_apps.keys():
			ApplicationsLoader._opened_apps[user] = UserRunningApps()
		ApplicationsLoader._opened_apps[user].add_app(app)
		CrequestMiddleware.get_request().updated_apps.add_top(app)

		with open('oppened-apps.dat', 'w') as f:
			dill.dump(self._opened_apps, f)
		
	