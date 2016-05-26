from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from punchclock.forms import TaskForm
from punchclock.models import Project, Activity, Task
from django.contrib.auth.models import User
from django.shortcuts import redirect
from punchclock import utils
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

    # if the user has a project they aer clocked into then send
    # them to switch tasks
    tasks = Task.objects.filter(user=user).filter(end_time=None)
    if tasks:
        return redirect('/punchclock/switch/')

    if request.method == 'GET':
        params['form'] = TaskForm()
        params['projects'] = Project.objects.all()
        return render_to_response('start_task.html',
                                  params,
                                  context_instance=RequestContext(request))
    else:  # request.method == 'POST'
        form = TaskForm(request.POST)
        if form.is_valid():
            current_task = utils.createNewTaskObject(request, form, user)
            params['in_time'] = current_task.start_time
            params['current_project'] = current_task.project
            params['current_activity'] = current_task.activity
            params['form'] = TaskForm()
            params['projects'] = Project.objects.all()
            return render_to_response('end_task.html',
                                      params,
                                      context_instance=RequestContext(request))


@login_required
def get_activities(request):
    chosen_project_name = request.GET['chosen_project']
    chosen_project = Project.objects.get(name=chosen_project_name)
    activities = chosen_project.activities.all()
    options = ""
    for activity in activities:
        new_option = "<option value='" + str(activity.name) + "'>" \
            + str(activity.name) + "</option>\n"
        options += new_option
    return HttpResponse(options)


@login_required
def switch_task(request):
    params = {'request': request}
    user = request.user
    params['user'] = user

    tasks = Task.objects.filter(user=user).filter(end_time=None)
    if not tasks:
        return redirect('/punchclock/')

    params['projects'] = Project.objects.all()

    if request.method == 'GET':
        params['form'] = TaskForm()
        return render_to_response('end_task.html',
                                  params,
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        # will get here if they are switching to another task
        tasks[0].end_time = datetime.datetime.now()
        tasks[0].save()
        form = TaskForm(request.POST)
        if form.is_valid():
            current_task = utils.createNewTaskObject(request, form, user)
            params['in_time'] = current_task.start_time
            params['current_project'] = \
                current_task.project.name.encode('utf8')
            params['current_activity'] = \
                current_task.activity.name.encode('utf8')
            return render_to_response('end_task.html',
                                      params,
                                      context_instance=RequestContext(request))


@login_required
def shift_details(request):
    params = {'request': request}
    c = {}
    c.update(csrf(request))
    user = request.user
    params['user'] = user
    tasks = Task.objects.filter(user=user).filter(end_time=None)
    if tasks:
        tasks[0].end_time = datetime.datetime.now()
        tasks[0].save()
    params['combine_tasks'], params['total'] = \
        utils.sumProjActivityPairs(user)

    return render_to_response('shift-details.html',
                              params,
                              context_instance=RequestContext(request))
