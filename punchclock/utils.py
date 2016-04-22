from punchclock.models import Project, Activity
from django.contrib.auth.models import User
import datetime

def createNewTaskObject(request, form, user):
    current_task = form.save(commit=False)
    current_task.user = user
    current_task.start_time = datetime.datetime.now()
    current_task.project = Project.objects.get(name=request.POST['project'])
    current_task.activity = Activity.objects.get(name=request.POST['activities'])
    current_task.save()
    return current_task
