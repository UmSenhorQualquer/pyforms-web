import inspect, os
from django.core.exceptions import ObjectDoesNotExist

try:
	from maestro.models import UserSettings
except:
	print("proscenium: maestro.models.UserSettings model does not exists")

class StorageManager:

	def __init__(self, modules):
		self._classes = {}
		self._storage = {}	
		self._default_module = modules[0]
		for modulename in modules:
			modules = modulename.split('.')
			moduleclass = __import__( '.'.join(modules[:-1]) , fromlist=[modules[-1]] )
			self._classes[modulename] = getattr(moduleclass, modules[-1])

		


	def get(self, user):
		if user.username not in self._storage:
			try:
				user_settings = UserSettings.objects.get(user=user)
				storage_manager = user_settings.user_storage
			except:
				storage_manager = self._default_module

			
			classdef = self._classes.get(storage_manager)
			self._storage[user.username] = classdef(user)
		
		return self._storage[user.username]
