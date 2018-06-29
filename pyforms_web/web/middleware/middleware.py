from .apps_2_update import Apps2Update
from confapp import conf
import threading, os, dill, filelock

class PyFormsMiddleware(object):
	_request = {}

	USER = None

	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.

	def __call__(self, request):
		# Code to be executed for each request before
		# the view (and later middleware) are called.
		request.updated_apps = Apps2Update()
		self.__class__._request[threading.current_thread()] = request

		response = self.get_response(request)

		# Code to be executed for each request/response after
		# the view is called.

		self.__class__._request.pop(threading.current_thread(), None)
		return response

	

	@classmethod
	def get_request(cls, default=None):
		"""Retrieve request"""
		return cls._request.get(threading.current_thread(), default)
	
	##################################################################################################
	##################################################################################################
	##################################################################################################
	@classmethod
	def user(cls): 		return cls.get_request().user

	@classmethod
	def add(cls, app): 	cls.get_request().updated_apps.add_top(app)
	
	@classmethod
	def get_instance(cls, app_id):
		user=cls.user()
		
		app_path = os.path.join(
			conf.PYFORMS_WEB_APPS_CACHE_DIR,
			'{0}-{1}'.format(user.pk, user.username),
			"{0}.app".format(app_id)
		)

		if os.path.isfile(app_path): 
			lock = filelock.FileLock(conf.PYFORMS_WEB_LOCKFILE)
			with lock.acquire(timeout=10):
				with open(app_path, 'rb') as f: 
					return dill.load(f)
		else:
			return None

	@classmethod
	def remove_instance(cls, app_id):
		user=cls.user()
		app_path = os.path.join(
			conf.PYFORMS_WEB_APPS_CACHE_DIR,
			'{0}-{1}'.format(user.pk, user.username),
			"{0}.app".format(app_id)
		)
		if os.path.isfile(app_path):
			lock = filelock.FileLock(conf.PYFORMS_WEB_LOCKFILE)
			with lock.acquire(timeout=10): 
				os.remove(app_path)
			return True
		else:
			return False
		


	##################################################################################################
	##################################################################################################
	##################################################################################################
