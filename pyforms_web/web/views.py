import os

import simplejson
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from pyforms_web.web import ApplicationsLoader
from pyforms_web.basewidget import custom_json_converter


@csrf_exempt
def upload_files(request):
    files_data = []
    files_metadata = []

    if request.method == 'POST':

        path2save = os.path.join(settings.MEDIA_ROOT, 'apps', request.POST['app_id'])

        for key in request.FILES:
            myfile = request.FILES[key]
            name = "".join([(c if c.isalnum() or c in ['.', '-', '_'] else '') for c in myfile.name])
            for c in r' []/\;,><&*:%=+@!#^()|?^': name = name.replace(c, '')

            fs = FileSystemStorage(location=path2save, base_url=settings.MEDIA_URL + 'apps/' + request.POST['app_id'] + '/')
            filename = fs.save(name, myfile)
            url = fs.url(filename)

            files_data.append(url)
            files_metadata.append({
                'date': fs.get_created_time(filename).strftime("%Y-%m-%d %H:%M:%S"),
                'extension': os.path.splitext(filename)[1],
                'file': url,
                'name': myfile.name,
                'old_name': myfile.name,
                'replaced': False,
                'size': fs.size(filename),
                'size2': fs.size(filename),
                'type': []
            })

    data = {'files': files_data, 'metas': files_metadata}
    return HttpResponse(simplejson.dumps(data, bigint_as_string=True, default=custom_json_converter), "application/json")


@never_cache
@csrf_exempt
def register_app(request, app_module):
    try:
        data = ApplicationsLoader.register_instance(request, app_module)
    except PermissionDenied as e:
        data = {'error': str(e)}
    if data is None:
        return HttpResponse(
            simplejson.dumps({'error': 'Application session ended.'}), "application/json"
        )
    return HttpResponse(simplejson.dumps(data, default=custom_json_converter), "application/json")


@never_cache
@csrf_exempt
def open_app(request, app_id):
    try:
        app = ApplicationsLoader.get_instance(request, app_id)
        params = {}
        params.update(app.init_form())

        for m in request.updated_apps.applications: m.commit()
    except PermissionDenied as e:
        params = {'error': str(e)}

    return HttpResponse(simplejson.dumps(params, default=custom_json_converter), "application/json")


@never_cache
@csrf_exempt
def update_app(request, app_id):
    data = simplejson.loads(request.body)
    data = ApplicationsLoader.update_instance(request, app_id, data)
    if data is None:
        return HttpResponse(simplejson.dumps(
            {'result': 'error', 'msg': 'Application session ended.'}),
            "application/json"
        )
    return HttpResponse(simplejson.dumps(data, default=custom_json_converter), "application/json")


@never_cache
@csrf_exempt
def remove_app(request, app_id):
    if ApplicationsLoader.remove_instance(request, app_id):
        data = {'res': 'OK'}
    else:
        data = {'res': 'ERROR', 'msg': 'the instance was not removed successfully'}
    return HttpResponse(simplejson.dumps(data, default=custom_json_converter), "application/json")


def app_stream(request, app_id, keyword=None):
    app = ApplicationsLoader.get_instance(request, app_id)

    response = StreamingHttpResponse(
        app.stream_status(request.user),
        content_type='text/event-stream',
        status=200)
    response['Cache-Control'] = 'no-cache'
    return response


def field_stream(request, app_id, fieldname, keyword=None):
    app = ApplicationsLoader.get_instance(request, app_id)
    field = getattr(app, fieldname)

    def stream():
        for d in field.streaming_func():
            yield f'data: {d}\n\n'

        app.commit(request.user)

    response = StreamingHttpResponse(
        stream(),
        content_type='text/event-stream',
        status=200)
    response['Cache-Control'] = 'no-cache'
    return response


@never_cache
@csrf_exempt
def autocomplete_search(request, app_id, fieldname, keyword=None):
    app = ApplicationsLoader.get_instance(request, app_id)
    field = getattr(app, fieldname)

    items = []
    if not field.multiple:
        items += [{'name': '---', 'value': None, 'text': '---'}] + items

    items += field.autocomplete_search(keyword)

    data = {'success': len(items) > 0, 'results': items}

    return HttpResponse(simplejson.dumps(data, default=custom_json_converter), "application/json")


@never_cache
@csrf_exempt
def controllist_queryset_export_csv(request, app_id, fieldname):
    app = ApplicationsLoader.get_instance(request, app_id)

    if app.has_export_csv_permissions(request.user):
        field = getattr(app, fieldname)
        if field.export_csv:
            return field.export_csv_http_response()
        else:
            return HttpResponse("It is not possible to export this queryset!")
    else:
        return HttpResponse("You have no permissions to export the queryset!")
