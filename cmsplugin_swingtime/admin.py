from django.contrib.contenttypes import generic
from django.contrib import admin
from cmsplugin_swingtime.models import *
from cms.admin.placeholderadmin import PlaceholderAdmin

#===============================================================================
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('label', 'abbr')
    prepopulated_fields = {"abbr": ("label",)}

#===============================================================================
#class GoogleCalendarAccountAdmin(admin.ModelAdmin):
#    model = GoogleCalendarAccount


#===============================================================================
class OccurrenceInline(admin.TabularInline):
    model = Occurrence
    extra = 1


#===============================================================================
class EventAdmin(PlaceholderAdmin):
    list_display = ('title', 'event_type', 'published')
    list_filter = ('event_type', )
    search_fields = ('title', )
    inlines = [OccurrenceInline]


#admin.site.register(GoogleCalendarAccount, GoogleCalendarAccountAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)