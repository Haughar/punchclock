from django import forms
from punchclock.models import Task

class TaskForm(forms.ModelForm):
    """ The form that submits a sign in / sign out / task switch of a shift.
    """
    class Meta:
        model = Task
        exclude = ('user', 'start_time', 'end_time', 'project', 'activity')
