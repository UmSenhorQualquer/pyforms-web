

PYFORMS_WEB_APPS_TIMEOUT   = 3600*48


PYFORMS_APPS = {}

LAYOUT_NEW_WINDOW = 2

try:
	import os
	from django.conf import settings

	PYFORMS_WEB_APPS_CACHE_DIR = os.path.join(settings.BASE_DIR,'apps-cache')
	PYFORMS_WEB_LOCKFILE 	   = os.path.join(settings.BASE_DIR,'lockfile.txt')
except:
	PYFORMS_WEB_APPS_CACHE_DIR = 'apps-cache'
	PYFORMS_WEB_LOCKFILE 	   = 'lockfile.txt'