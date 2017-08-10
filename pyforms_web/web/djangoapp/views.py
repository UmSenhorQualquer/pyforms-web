from django.http 					import HttpResponse
from django.shortcuts 				import render_to_response
from django.template 				import RequestContext
from django.views.decorators.cache	import never_cache
from django.views.decorators.csrf 	import csrf_exempt
from django.middleware.csrf 		import get_token
from pyforms_web.web.djangoapp 		import ApplicationsLoader
from pysettings 					import conf
import json, simplejson, os, re
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

@csrf_exempt
def upload_files(request):

	files_data 		= []
	files_metadata 	= []

	if request.method == 'POST':

		path2save = os.path.join(settings.MEDIA_ROOT, 'apps',request.POST['app_id'])

		for key in request.FILES:
			myfile = request.FILES[key]
			name   = slugify(myfile.name)
			for c in r' []/\;,><&*:%=+@!#^()|?^': name = name.replace(c,'')
			fs 			= FileSystemStorage(location=path2save, base_url=settings.MEDIA_URL+'apps/'+request.POST['app_id']+'/')
			filename 	= fs.save(name, myfile)
			url 		= fs.url(filename)

			files_data.append(url)
			files_metadata.append({
				'date':fs.created_time(filename).strftime("%Y-%m-%d %H:%M:%S"),
				'extension':os.path.splitext(filename)[1],
				'file':url,
				'name':myfile.name,
				'old_name':myfile.name,
				'replaced':False,
				'size':fs.size(filename),
				'size2':fs.size(filename),
				'type':[]
			})

	data = {'files':files_data, 'metas':files_metadata  }
	return HttpResponse(simplejson.dumps(data,bigint_as_string=True ), "application/json")


def filesbrowser_browse(request):
	application = 'pyforms_web.web.djangoapp.filesbrowser.FilesBrowserApp'
	
	app = ApplicationsLoader.create_instance(request, application)
	params = { 'application': application, 'appInstance': app, 'csrf_token': get_token(request)}
	params.update( app.init_form() )

	try:
		#For django versions < 1.10
		return render_to_response(conf.PYFORMS_WEB_APPS_TEMPLATE_NO_TITLE,params, context_instance=RequestContext(request))
	except:
		#For django versions => 1.10
		return render_to_response(conf.PYFORMS_WEB_APPS_TEMPLATE_NO_TITLE,params)


def register_app(request, app_module):
	try:
		data = ApplicationsLoader.register_instance(request, app_module)
	except PermissionDenied as e:
		data = {'error': str(e)}
	if data is None: 
		return HttpResponse(
			simplejson.dumps({'error':'Application session ended.'}), "application/json"
		)
	return HttpResponse(simplejson.dumps(data), "application/json")


def open_app(request, app_id):
	try:
		app  	= ApplicationsLoader.get_instance(request, app_id)
		params 	= {}
		params.update( app.init_form() )

		for m in request.updated_apps.applications: m.commit()
	except PermissionDenied as e:
		params = {'error': str(e)}
	
	return HttpResponse(simplejson.dumps(params), "application/json")
	

@never_cache
@csrf_exempt
def update_app(request, app_id):
	print('---------')
	print(request.POST)
	print(request.GET)
	print(request.body)
	data = simplejson.loads(request.body)
	data = ApplicationsLoader.update_instance(request, app_id, data)
	if data is None:  
		return HttpResponse(simplejson.dumps(
			{'result':'error', 'msg':'Application session ended.'}), 
			"application/json"
		)
	return HttpResponse(simplejson.dumps(data), "application/json")


@never_cache
@csrf_exempt
def remove_app(request, app_id):
	if ApplicationsLoader.remove_instance(request, app_id):
		data = {'res':'OK'}
	else:
		data = {'res': 'ERROR', 'msg': 'the instance was not removed successfully'}
	return HttpResponse(simplejson.dumps(data), "application/json")

