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
    Add a data point to a signal
    """
    if request.POST:
        try:
            value = request.POST
            signal = Signal.objects.get(signal_id=signal_id)
            signal.add_point(value)
            response_dict = {'status': 'succeeded'}
            return HttpResponse(response_dict, status=200, content_type="application/json")
        except BaseException as e:
            return HttpResponse({'status': 'failed{}'.format(e)}, status=500)