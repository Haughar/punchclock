from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from punchclock.forms import TaskForm
import datetime


@login_required
def start_task(request):
    params = {'request': request}
    # Generate a token to protect from cross-site request forgery
    c = {}
    c.update(csrf(request))

    # Grab information we want to pass along no matter what state we're in
    user = request.user
    params['user'] = user

    if request.method == 'GET':
        params['form'] = TaskForm()
        return render_to_response('start_task.html',
                                  params,
                                  context_instance=RequestContext(request))
    else: # request.method == 'POST'
        form = TaskForm(request.POST)
        if form.is_valid():
            current_task = formsave(commit=False)
            current_task.person = user
            current_task.start_time = datetime.now()
            current_task.save()
            params['in_time'] = current_task.start_time
            params['project'] = current_task.project
            params['activity'] = current_task.activity
            return render_to_response('end_task.html',
                                      params,
                                      context_instance=RequestContext(request))
