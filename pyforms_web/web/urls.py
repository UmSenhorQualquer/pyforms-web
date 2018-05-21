from django.conf.urls 				import url
from pyforms_web.web.views 	import update_app, remove_app
from pyforms_web.web.views 	import register_app, open_app, upload_files
from pyforms_web.web.views 	import autocomplete_search


urlpatterns = [
	url(r'^app/register/(?P<app_module>[a-zA-Z._\- 0-9]+)/', register_app	),
	url(r'^app/open/(?P<app_id>[a-zA-Z._\- 0-9]+)/', 		 open_app		),
	url(r'^app/update/(?P<app_id>[a-zA-Z._\- 0-9]+)/',		 update_app		),
	url(r'^app/remove/(?P<app_id>[a-zA-Z._\- 0-9]+)/', 		 remove_app		),
	url(r'^autocomplete/(?P<app_id>[a-zA-Z._\- 0-9]+)/(?P<fieldname>[a-zA-Z._\- 0-9]+)/(?P<keyword>[a-zA-Z._\- 0-9]+)/',     autocomplete_search	),
	url(r'^autocomplete/(?P<app_id>[a-zA-Z._\- 0-9]+)/(?P<fieldname>[a-zA-Z._\- 0-9]+)/',     autocomplete_search	),
	url(r'^upload-files/', upload_files	),
]