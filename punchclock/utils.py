from punchclock.models import Project, Activity, Task
from django.contrib.auth.models import User
import datetime


def createNewTaskObject(request, form, user):
    current_task = form.save(commit=False)
    current_task.user = user
    current_task.start_time = datetime.datetime.now()
    current_task.project = Project.objects.get(name=request.POST['project'])
    current_task.activity = \
        Activity.objects.get(name=request.POST['activities'])
    current_task.save()
    return current_task


def sumProjActivityPairs(user):
    tasks = Task.objects.filter(
        user=user,
        start_time__year=datetime.datetime.today().year,
        start_time__month=datetime.datetime.today().month,
        start_time__day=datetime.datetime.today().day)
    combine_tasks = {}
    total = datetime.timedelta(0)
    for task in tasks:
        name = task.project.name + ", " + task.activity.name
        if name in combine_tasks:
            combine_tasks[name] += (task.end_time - task.start_time)
        else:
            combine_tasks[name] = (task.end_time - task.start_time)
        total += (task.end_time - task.start_time)
    return (combine_tasks, total)
