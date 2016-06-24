import inspect, sys

class ApplicationsLoader:

	_storage = {}

	@staticmethod
	def createInstance(modulename):

		if modulename not in ApplicationsLoader._storage:
			modules = modulename.split('.')
			moduleclass = __import__( '.'.join(modules[:-1]) , fromlist=[modules[-1]] )
			ApplicationsLoader._storage[modulename] = getattr(moduleclass, modules[-1])
		
		moduleclass = ApplicationsLoader._storage[modulename]

		obj = moduleclass()
		obj.modulename = modulename
		return obj

