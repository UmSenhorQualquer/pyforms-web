from django.conf.urls 				import url
from pyforms_web.web.django.views 	import *

urlpatterns = [ 
	url(r'^update/(?P<application>[a-zA-Z._ 0-9]+)/', 	updateapplicationform),
	url(r'^filesbrowser/', 					filesbrowser_browse),
]