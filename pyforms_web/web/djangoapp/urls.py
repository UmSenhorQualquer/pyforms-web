from django.conf.urls 				import url
from pyforms_web.web.djangoapp.views 	import update_app, remove_app, filesbrowser_browse, register_app, open_app, upload_files

urlpatterns = [
	url(r'^app/register/(?P<app_module>[a-zA-Z._\- 0-9]+)/', register_app	),
	url(r'^app/open/(?P<app_id>[a-zA-Z._\- 0-9]+)/', 		 open_app		),
	url(r'^app/update/(?P<app_id>[a-zA-Z._\- 0-9]+)/',		 update_app		),
	url(r'^app/remove/(?P<app_id>[a-zA-Z._\- 0-9]+)/', 		 remove_app		),
	url(r'^upload-files/', upload_files	),	
	url(r'^filesbrowser/', filesbrowser_browse),
]