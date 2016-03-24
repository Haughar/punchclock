from django.db import models
from django.contrib.auth.models import User
import datetime


class Activity(models.Model):
    """ Specific activities that a user can work on within
        a project.
    """
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


class Project(models.Model):
    """ A broad category that contains activites that
        a user can work on during the day.
    """
    name = models.CharField(max_length=256)
    activities = models.ManyToManyField(Activity)

    def __unicode__(self):
        return self.name


class Task(models.Model):
    """ A collection of all the project/activities that a
        user worked on in a day.
    """
    user = models.ForeignKey(User, related_name='uwnetid')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    project = models.ForeignKey(Project)
    activity = models.ForeignKey(Activity)


    def __unicode__(self):
        return "%s %s-%s" % (self.user, self.start_time, self.end_time)
