from django.conf.urls import *

urlpatterns = patterns('punchclock.views',
                       url(r'^$', 'start_time'),
                       )
