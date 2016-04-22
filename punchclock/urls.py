from django.conf.urls import *

urlpatterns = patterns('punchclock.views',
                       url(r'^$', 'start_task'),
                       url(r'^switch/$', 'switch_task'),
                       url(r'^activities/$', 'get_activities'),
                       url(r'^shift-details/$', 'shift_details'),
                       )
