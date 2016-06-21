from django.conf.urls 			import url
from pyforms_web.web.django.views 	import updateapplicationform

urlpatterns = [ url(r'^update/(?P<application>\w+)/', updateapplicationform) ]