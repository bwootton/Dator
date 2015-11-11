import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from data_api.models import Signal, Blob



def noop_view(request):
    c={}
    c.update(csrf(request))
    return render_to_response('noop.html', c)

@csrf_exempt
def blob_data(request, blob_id):
    """
    Set or get data for a json blob.
    :param request:
    :param blob_id:
    :return:
    """
    try:
        json_blob = Blob.objects.get(id=blob_id)
    except Blob.DoesNotExist as e:
        return HttpResponse({'status: failed - Blob requested does not exist.'}, status=404)
    if request.method=='POST':
        try:
            json_blob.set_data(request.body)
            response_dict={'status': 'succeeded'}
            return HttpResponse(response_dict, status=200, content_type='application/json')
        except BaseException as e:
            return HttpResponse({'status': 'failed {}'.format(e)}, status=500)
    elif request.method == 'GET':
        try:
            body = json_blob.get_data()
            return HttpResponse(body, status=200, content_type="application/octet-stream")
        except BaseException as e:
            return HttpResponse({'status': 'failed {}'.format(e)}, status=500)

def signal_data(request, signal_id):
    """
    Add data points to or get a signal. Incoming/Outgoing signal in json body.  Format:
    [[<value>,<utc time in millisec since epoch>], ...]
    signal points must be in ascending order of occurence.
    """
    try:
        signal = Signal.objects.get(id=signal_id)
    except Signal.DoesNotExist as e:
        return HttpResponse({'status': 'failed - Signal requested does not exist'}, status=404)

    if request.method=='POST':
        try:
            data = json.loads(request.body)
            signal.add_points(data)
            response_dict = {'status': 'succeeded'}
            return HttpResponse(response_dict, status=200, content_type="application/json")
        except BaseException as e:
            return HttpResponse({'status': 'failed{}'.format(e)}, status=500)

    elif request.method == 'GET':
        try:
            body = json.dumps(signal.get_data())
            return HttpResponse(body, status=200, content_type="application/json")
        except BaseException as e:
            return HttpResponse({'status': 'failed {}'.format(e)}, status=500)

