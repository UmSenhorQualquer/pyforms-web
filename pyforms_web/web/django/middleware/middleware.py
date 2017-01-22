from pyforms_web.web.django.middleware.apps_2_update import Apps2Update
from pyforms_web.web.django.middleware.user_apps import UserApps
import threading


class PyFormsMiddleware(object):
	_request 		= {}
	_applications 	= {}
	_session_active = {}
	
	def process_request(self, request):
		"""Store request"""
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

	@classmethod
	def user(cls): return cls.get_request().user


	@classmethod
	def __add__(cls, app):
		user = cls.user()
		if cls._session_active.get(user, False):
			if user not in cls._applications: cls._applications[user] = {}
			cls._applications[user][app.uid] = app
		return cls

	@classmethod
	def __sub__(cls):
		user = cls.user()
		if user not in cls._applications: 	   return cls
		if app.uid in cls._applications[user]: del cls._applications[user][app.uid]

	##################################################################################################
	##################################################################################################
	##################################################################################################

	@classmethod
	def start_session(cls):
		user=cls.user()
		cls._session_active[user]=Apps2Update()

	@classmethod
	def register_update(cls, app, top=False):
		user=cls.user()
		app2update = cls._session_active[user]
		if top:
			app2update.add_top(app)
		else:
			app2update.add_bottom(app)

	@classmethod
	def updated_applications(cls):
		return cls._session_active[user].applications

	@classmethod
	def commit(csl): cls._session_active[user]=False

	##################################################################################################
	##################################################################################################
	##################################################################################################
