

class UserApps(object):

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