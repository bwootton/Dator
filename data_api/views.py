import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from data_api.models import Signal


def simple_view(request):
    return render(request, 'simple_view.html')


def root_view(request):
    return render(request, 'root_view.html')


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

    elif request.method=='GET':
        try:
            body = json.dumps(signal.get_data())
            return HttpResponse(body, status=200, content_type="application/json")
        except BaseException as e:
            return HttpResponse({'status': 'failed {}'.format(e)}, status=500)

