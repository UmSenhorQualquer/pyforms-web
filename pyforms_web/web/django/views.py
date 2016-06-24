from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.views.decorators.cache 			import never_cache
from django.views.decorators.csrf 			import csrf_exempt
import json, simplejson, os
from django.contrib.staticfiles.views import serve
from pyforms_web.web.django import ApplicationsLoader

@never_cache
@csrf_exempt
def updateapplicationform(request, application):
	module 				= ApplicationsLoader.createInstance(application)
	module.httpRequest 	= request

	module.loadSerializedForm( json.loads(request.body) )
	
	result 				= module.serializeForm()

	return HttpResponse(simplejson.dumps(result), "application/json")



from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.shortcuts import render_to_response
import os, simplejson
from django.conf import settings
from django.http import HttpResponse

from django.middleware.csrf import get_token

from jfu.http import upload_receive, UploadResponse, JFUResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseServerError
import simplejson, json, glob, os
from django.conf import settings
import time, shlex

def sizeof_fmt(num):
	for x in ['bytes','KB','MB','GB']:
		if num < 1000.0: return "%3.1f%s" % (num, x)
		num /= 1000.0
	return "%3.1f%s" % (num, 'TB')

def filesbrowser_browse(request):
	application = 'pyforms_web.web.django.filesbrowser.FilesBrowserApp'
	app = ApplicationsLoader.createInstance(application)
	app.httpRequest = request
	
	params = { 'application': application, 'appInstance': app, 'csrf_token': get_token(request)}
	params.update( app.initForm() )

	return render_to_response(
		os.path.join('pyforms', 'pyforms-template-no-title.html'),
		params, context_instance=RequestContext(request))