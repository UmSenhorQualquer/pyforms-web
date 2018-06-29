

PYFORMS_WEB_APPS_TIMEOUT   = 3600*48


PYFORMS_APPS = {}


try:
	import os
	from django.conf import settings

	PYFORMS_WEB_APPS_CACHE_DIR = os.path.join(settings.BASE_DIR,'apps-cache')
except:
	PYFORMS_WEB_APPS_CACHE_DIR = 'apps-cache'