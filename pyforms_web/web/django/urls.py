from django.conf.urls 			import patterns, url
from pyforms_web.web.django.views 	import updateapplicationform

urlpatterns = patterns('',
	url(r'^update/(?P<application>\w+)/', updateapplicationform),
)