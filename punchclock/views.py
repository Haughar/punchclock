from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):

    params = {'request': request}
    return render_to_response('home.html', params, context_instance=RequestContext(request))
