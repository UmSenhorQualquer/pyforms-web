from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache 			import never_cache
from django.views.decorators.csrf 			import csrf_exempt
import json, simplejson, os
from django.contrib.staticfiles.views import serve
from pyforms_web.web.django import ApplicationsLoader

class Apps2Update(object):

	def __init__(self):
		self._top_apps = []
		self._bottom_apps = []

	def add_top(self, app):
		if app in self._bottom_apps: return
		if app in self._top_apps: return

		self._top_apps.append(app)

	def add_bottom(self, app):
		if app in self._top_apps: self._top_apps.remove(app)
		if app in self._bottom_apps: return
		
		self._bottom_apps.append(app)

	@property
	def applications(self): return self._top_apps+self._bottom_apps

@never_cache
@csrf_exempt
def removeapplicationform(request, application_id):
	data = ApplicationsLoader.remove_instance(request, application_id)
	return HttpResponse(simplejson.dumps({'res':'OK'}), "application/json")


@never_cache
@csrf_exempt
def updateapplicationform(request, application_id):
	data = json.loads(request.body)
	data = ApplicationsLoader.update_instance(request, application_id, data)
	if data is None:  return HttpResponse(simplejson.dumps({'error':'Application session ended.'}), "application/json")
	return HttpResponse(simplejson.dumps(data), "application/json")



from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.shortcuts import render_to_response
import os, simplejson
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
import time, shlex

def sizeof_fmt(num):
	for x in ['bytes','KB','MB','GB']:
		if num < 1000.0: return "%3.1f%s" % (num, x)
		num /= 1000.0
	return "%3.1f%s" % (num, 'TB')

def filesbrowser_browse(request):
	application = 'pyforms_web.web.django.filesbrowser.FilesBrowserApp'
	
	app = ApplicationsLoader.create_instance(request, application)
	params = { 'application': application, 'appInstance': app, 'csrf_token': get_token(request)}
	params.update( app.init_form() )

	try:
		#For django versions < 1.10
		return render_to_response(os.path.join('pyforms', 'pyforms-template-no-title.html'),params, context_instance=RequestContext(request))
	except:
		#For django versions => 1.10
		return render_to_response(os.path.join('pyforms', 'pyforms-template-no-title.html'),params)