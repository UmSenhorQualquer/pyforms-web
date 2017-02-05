from pyforms_web.web.django.middleware.apps_2_update import Apps2Update
from pysettings import conf
import threading, os, dill

class PyFormsMiddleware(object):
	_request = {}
	
	def process_request(self, request):
		"""Store request"""
		request.updated_apps = Apps2Update()
		self.__class__.set_request(request)
		
	def process_response(self, request, response):
		"""Delete request"""
		self.__class__.del_request()
		return response

	def process_exception(self, request, exception):
		"""Delete request"""
		self.__class__.del_request()

	@classmethod
	def get_request(cls, default=None):
		"""Retrieve request"""
		return cls._request.get(threading.current_thread(), default)

	@classmethod
	def set_request(cls, request):
		"""Store request"""
		cls._request[threading.current_thread()] = request

	@classmethod
	def del_request(cls):
		"""Delete request"""
		cls._request.pop(threading.current_thread(), None)

	
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
			with open(app_path, 'rb') as f: 
				return dill.load(f)
		else:
			return None
		


	##################################################################################################
	##################################################################################################
	##################################################################################################
