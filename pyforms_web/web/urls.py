from django.urls import re_path
from pyforms_web.web.views import update_app, remove_app
from pyforms_web.web.views import register_app, open_app, upload_files
from pyforms_web.web.views import autocomplete_search
from pyforms_web.web.views import controllist_queryset_export_csv
from pyforms_web.web.views import field_stream, app_stream


urlpatterns = [
	re_path(r'^app/register/(?P<app_module>[a-zA-Z._\- 0-9]+)/', register_app	),
	re_path(r'^app/open/(?P<app_id>[a-zA-Z._\- 0-9]+)/', 		 open_app		),
	re_path(r'^app/update/(?P<app_id>[a-zA-Z._\- 0-9]+)/',		 update_app		),
	re_path(r'^app/remove/(?P<app_id>[a-zA-Z._\- 0-9]+)/', 		 remove_app		),
	re_path(r'^export-csv/(?P<app_id>[a-zA-Z._\- 0-9]+)/(?P<fieldname>[a-zA-Z._\- 0-9]+)/', controllist_queryset_export_csv	),
	re_path(r'^autocomplete/(?P<app_id>[a-zA-Z._\- 0-9]+)/(?P<fieldname>[a-zA-Z._\- 0-9]+)/(?P<keyword>[a-zA-Z._\- 0-9]+)/',     autocomplete_search	),
	re_path(r'^autocomplete/(?P<app_id>[a-zA-Z._\- 0-9]+)/(?P<fieldname>[a-zA-Z._\- 0-9]+)/', autocomplete_search),
	re_path(r'^field-stream/(?P<app_id>[a-zA-Z._\- 0-9]+)/(?P<fieldname>[a-zA-Z._\- 0-9]+)/', field_stream),
	re_path(r'^app-stream/(?P<app_id>[a-zA-Z._\- 0-9]+)/', app_stream),
	re_path(r'^upload-files/', upload_files	),
]