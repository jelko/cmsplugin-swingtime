from django.contrib.contenttypes import generic
from django.contrib import admin
from cmsplugin_swingtime.models import *
from cms.admin.placeholderadmin import PlaceholderAdmin



#===============================================================================
#class GoogleCalendarAccountAdmin(admin.ModelAdmin):
#    model = GoogleCalendarAccount


#===============================================================================
class OccurrenceInline(admin.TabularInline):
    model = Occurrence
    extra = 1


#===============================================================================
class EventAdmin(PlaceholderAdmin):
    list_display = ('title', 'published')
    search_fields = ('title',)
    inlines = [OccurrenceInline]


#admin.site.register(GoogleCalendarAccount, GoogleCalendarAccountAdmin)
admin.site.register(Event, EventAdmin)
