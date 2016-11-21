import datetime, json
from pysettings import conf

class UserRunningApps(object):

	def __init__(self):
		self._apps = {}

	def add_app(self, app):
		print self._apps
		if app.uid in self._apps.keys(): return
		self._apps[app.uid] = [datetime.datetime.now(), app]
		
		
	def get_app(self, app_id): 
		self.__garbage_collector()
		
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
	def createInstance(modulename, user, data=None):
		if data is not None:
			app  = ApplicationsLoader._opened_apps[user].get_app(data['uid'])
		else:
			if modulename not in ApplicationsLoader._storage:
				modules = modulename.split('.')
				moduleclass = __import__( '.'.join(modules[:-1]) , fromlist=[modules[-1]] )
				ApplicationsLoader._storage[modulename] = getattr(moduleclass, modules[-1])
			
			moduleclass = ApplicationsLoader._storage[modulename]

			app = moduleclass()

			
		return app

	@staticmethod
	def add_app(user, app):
		# register the application globaly
		if user not in ApplicationsLoader._opened_apps.keys():
			ApplicationsLoader._opened_apps[user] = UserRunningApps()
		ApplicationsLoader._opened_apps[user].add_app(app)
		
	