from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('cmsplugin_swingtime',
    url(r'^$', 'views.eventIndexView', name="swingtime-index"),
    url(r'^archiv/$', 'views.eventArchiveView', name="swingtime-archive"),
    url(r'^(?P<event_type>[-\w\d]+)/$', 'views.eventTypeView', name="swingtime-type-index"),
    url(r'^(?P<event_type>[-\w\d]+)/(?P<event_id>\d+)/$', 'views.eventView', name="swingtime-event"),
)

