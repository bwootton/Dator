import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from robots.models import Signal


def simple_view(request):
    return render(request, 'simple_view.html')


def root_view(request):
    return render(request, 'root_view.html')


def add_signal_data(request, signal_id):
    """
    Add a data point to a signal. Incoming signal in json body.  Format:
    [[<value>,<time in millisec since epoch>], ...]
    signal points must be in ascending order of occurence.
    """
    if request.POST:
        try:
            data = json.loads(request.body)
            signal = Signal.objects.get(signal_id=signal_id)
            for datum in data:
                signal.add_point(datum[0], datum[1])
            response_dict = {'status': 'succeeded'}
            return HttpResponse(response_dict, status=200, content_type="application/json")
        except BaseException as e:
            return HttpResponse({'status': 'failed{}'.format(e)}, status=500)