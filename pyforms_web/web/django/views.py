from django.http 					import HttpResponse
from django.shortcuts 				import render_to_response
from django.template 				import RequestContext
from django.views.decorators.cache	import never_cache
from django.views.decorators.csrf 	import csrf_exempt
from django.middleware.csrf 		import get_token
from pyforms_web.web.django 		import ApplicationsLoader
from pysettings 					import conf
import json, simplejson, os




def filesbrowser_browse(request):
	application = 'pyforms_web.web.django.filesbrowser.FilesBrowserApp'
	
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
	data = ApplicationsLoader.register_instance(request, app_module)
	if data is None: 
		return HttpResponse(
			simplejson.dumps({'error':'Application session ended.'}), "application/json"
		)
	return HttpResponse(simplejson.dumps(data), "application/json")


def open_app(request, app_id):	
	app  	= ApplicationsLoader.get_instance(request, app_id)
	params 	= {'appInstance': app}
	params.update( app.init_form() )
	return render_to_response(conf.PYFORMS_WEB_APPS_TEMPLATE, params)
	

@never_cache
@csrf_exempt
def update_app(request, app_id):
	data = json.loads(request.body)
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
	data = ApplicationsLoader.remove_instance(request, app_id)
	return HttpResponse(simplejson.dumps({'res':'OK'}), "application/json")

