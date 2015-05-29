from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def simple_view(request):
    return render(request, 'simple_view.html')

def root_view(request):
    return render(request, 'root_view.html')