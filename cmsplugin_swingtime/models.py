import pytz

from datetime import datetime, date, timedelta

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

from cms.models.fields import PlaceholderField

#import gdata.service
#import gdata.calendar.service

#from icalendar.cal import Calendar

from dateutil import rrule


__all__ = (
#  'GoogleCalendarAccount',
  'EventType',
  'Event',
  'Occurrence',
  'create_event'
)

_services = {}


rrule_days = {
  'SU': rrule.SU,
  'MO': rrule.MO,
  'TU': rrule.TU,
  'WE': rrule.WE,
  'TH': rrule.TH,
  'FR': rrule.FR,
  'SA': rrule.SA
}

#class GoogleCalendarAccount(models.Model):
#  email = models.CharField(max_length = 100)
#  password = models.CharField(max_length = 100)
#
#  class Meta:
#    verbose_name = _('google calendar account')
#    verbose_name_plural = _('google calendar accounts')
#
#  def _get_service(self):
#    if not _services.has_key(self.email):
#      _service = gdata.calendar.service.CalendarService()
#      #_service.source = 'ITSLtd-Django_Google-%s' % VERSION
#      _service.email = self.email
#      _service.password = self.password
#      _service.ProgrammaticLogin()
#      _services[self.email] = _service
#    return _services[self.email]
#  service = property(_get_service, None)
#
#  def get_own_calendars(self):
#    cals = self.service.GetOwnCalendarsFeed()
#    result = []
#    for i, cal in enumerate(cals.entry):
#      result.append(cal)
#    return result
#
#  def get_events(self):
#    result = []
#    for cal in self.get_own_calendars():
#      for link in cal.link:
#        if link.rel == 'alternate':
#          events =  self.service.GetCalendarEventFeed(uri = link.href)
#          for i, event in enumerate(events.entry):
#            result.append(event)
#    return result


#@receiver(signals.post_save, sender=GoogleCalendarAccount)
#def sync_events(sender, instance, created, **kwargs):
#  '''
#  Synchronizes events for the saved calendar.
#  '''
#  for gevent in instance.get_events():
#    # get or create this event in the DB
#    event, created = Event.objects.get_or_create(uri=gevent.id.text)
#    # update title and description
#    event.title = gevent.title.text
#    event.description = gevent.content.text
#    if gevent.where:
#      event.where = gevent.where[0].value_string
#    event.save()
#
#    stale_occurrences = []
#    if gevent.recurrence and gevent.recurrence.text:
#      # manage recurrences (if any)
#      recurrence_ical_data = 'BEGIN:VCALENDAR\n%s\nEND:VCALENDAR' % gevent.recurrence.text
#      parsed_recurrence = Calendar.from_ical(recurrence_ical_data)
#      start_time = parsed_recurrence['DTSTART'].dt
#      end_time = parsed_recurrence['DTEND'].dt
#      rrules = dict(parsed_recurrence['RRULE'])
#      # add a default count to rrule to bound it unless a bound is specified
#      if not (('COUNT' in rrules) or ('UNTIL' in rrules)):
#        rrules['count'] = 52
#      occurrence_pks = event.add_occurrences(start_time, end_time, **rrules)
#      stale_occurrences = event.occurrence_set.exclude(pk__in=occurrence_pks)
#    elif gevent.when:
#      # otherwise just do a single-occurrence event
#      occurrence_pks = event.add_occurrences(gevent.when[0].start_time, gevent.when[0].end_time)
#      stale_occurrences = event.occurrence_set.exclude(pk__in=occurrence_pks)
#
#    # Clear out any stale occurrences.
#    # Note:  only occurrences with end times in the future will be removed,
#    # since past occurrences may have data already associated with them.
#    for occurrence in stale_occurrences:
#      if occurrence.end_time > timezone.now():
#        occurrence.delete()

#===============================================================================
class EventType(models.Model):
    '''
    Simple ``Event`` classifcation.
    
    '''
    label = models.CharField(_('label'), max_length=50)
    abbr = models.SlugField(_('slug'), unique=True)

    #===========================================================================
    class Meta:
        verbose_name = _('event type')
        verbose_name_plural = _('event types')
        
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.label

#===============================================================================
class Event(models.Model):
  '''
  Container model for general metadata and associated ``Occurrence`` entries.
  '''
  title = models.CharField(_('title'), max_length=100)
  where = models.CharField(_('where'), max_length=100, blank=True, null=True)
  description = PlaceholderField('description', related_name='event_description', verbose_name=_('description'))
  event_type = models.ForeignKey(EventType, verbose_name=_('event type'))
  uri = models.URLField(_('URL'), blank=True, null=True)
  published = models.BooleanField(_('published'), default=True)

  #===========================================================================
  class Meta:
    verbose_name = _('event')
    verbose_name_plural = _('events')
    ordering = ('title', )

  #---------------------------------------------------------------------------
  def __unicode__(self):
    return self.title

  #---------------------------------------------------------------------------
  @models.permalink
  def get_absolute_url(self):
    return ('swingtime-event', (), {'event_type': str(self.event_type.abbr), 'event_id': str(self.id)})

  #---------------------------------------------------------------------------
  def add_occurrences(self, start_time, end_time, **rrule_params):
    '''
    Add one or more occurences to the event using a comparable API to
    ``dateutil.rrule``.

    If ``rrule_params`` does not contain a ``freq``, one will be defaulted
    to ``rrule.DAILY``.

    Because ``rrule.rrule`` returns an iterator that can essentially be
    unbounded, we need to slightly alter the expected behavior here in order
    to enforce a finite number of occurrence creation.

    If both ``count`` and ``until`` entries are missing from ``rrule_params``,
    only a single ``Occurrence`` instance will be created using the exact
    ``start_time`` and ``end_time`` values.

    Returns a queryset of occurrences created or matched.
    '''
    for key in rrule_params.keys():
      rrule_value = rrule_params[key]
      if type(rrule_value) == list:
        # because for whatever reason, the value could be a list
        rrule_value = rrule_value[0]
      try:
        rrule_value = getattr(rrule, rrule_value.upper(), rrule_value)
      except:
        pass

      if key.lower() != 'byday':
        rrule_params[key.lower()] = rrule_value
        if key.lower() != key:
          del rrule_params[key]
      else:
        # some weekday values include numbers which aren't parsed by our
        # handy library by default, so we parse them out here
        if isinstance(rrule_value, str):
          day_function = rrule_days[rrule_value[-2:]]
          if len(rrule_value) > 2:
            value = int(rrule_value[:-2])
            rrule_value = day_function(value)
          else:
            rrule_value = day_function()
        rrule_params['byweekday'] = rrule_value
        del rrule_params[key]

    tz = timezone.get_default_timezone()
    occurrence_pks = []
    if 'count' not in rrule_params and 'until' not in rrule_params:
      occurrence, created = self.occurrence_set.get_or_create(start_time=start_time, end_time=end_time)
      occurrence_pks += [occurrence.pk]
    else:
      delta = end_time - start_time
      for ev in rrule.rrule(dtstart=start_time, **rrule_params):
        # recalculate and localize the date, because we may cross a DST boundary
        # apparently, rrule doesn't really care about DST
        newtime = datetime(ev.year, ev.month, ev.day, ev.hour, ev.minute, ev.second)
        newtime = tz.localize(newtime).astimezone(pytz.UTC)
        try:
          occurrence, created = self.occurrence_set.get_or_create(start_time=newtime, end_time=newtime + delta)
        except:
          occurrence, created = self.occurrence_set.get_or_create(start_time=ev, end_time=ev + delta)
        occurrence_pks += [occurrence.pk]

    return occurrence_pks

  #---------------------------------------------------------------------------
  def upcoming_occurrences(self):
    '''
    Return all occurrences that are set to start on or after the current
    time.
    '''
    return self.occurrence_set.filter(start_time__gte=datetime.now())

  #---------------------------------------------------------------------------
  def next_occurrence(self):
    '''
    Return the single occurrence set to start on or after the current time
    if available, otherwise ``None``.
    '''
    upcoming = self.upcoming_occurrences()
    return upcoming and upcoming[0] or None

  #---------------------------------------------------------------------------
  def daily_occurrences(self, dt=None):
    '''
    Convenience method wrapping ``Occurrence.objects.daily_occurrences``.
    '''
    return Occurrence.objects.daily_occurrences(dt=dt, event=self)

#===============================================================================
class OccurrenceManager(models.Manager):

  use_for_related_fields = True

  #---------------------------------------------------------------------------
  def daily_occurrences(self, dt=None, event=None):
    '''
    Returns a queryset of for instances that have any overlap with a
    particular day.

    * ``dt`` may be either a datetime.datetime, datetime.date object, or
      ``None``. If ``None``, default to the current day.

    * ``event`` can be an ``Event`` instance for further filtering.
    '''
    dt = dt or datetime.now()
    start = datetime(dt.year, dt.month, dt.day)
    end = start.replace(hour=23, minute=59, second=59)
    qs = self.filter(
      models.Q(
        start_time__gte=start,
        start_time__lte=end,
      ) |
      models.Q(
        end_time__gte=start,
        end_time__lte=end,
      ) |
      models.Q(
        start_time__lt=start,
        end_time__gt=end
      )
    )

    return qs.filter(event=event) if event else qs


#===============================================================================
class Occurrence(models.Model):
  '''
  Represents the start end time for a specific occurrence of a master ``Event``
  object.
  '''
  start_time = models.DateTimeField(_('start time'))
  end_time = models.DateTimeField(_('end time'))
  event = models.ForeignKey(Event, verbose_name=_('event'), editable=False)
  hide_time = models.BooleanField(verbose_name=_('hide time in frontend'), help_text=_('use this checkbox to hide start and end time in the frontend. A value has to be provided anyway!'))

  objects = OccurrenceManager()

  #===========================================================================
  class Meta:
    verbose_name = _('occurrence')
    verbose_name_plural = _('occurrences')
    ordering = ('start_time', 'end_time')

  #---------------------------------------------------------------------------
  def __unicode__(self):
    return u'%s: %s' % (self.title, self.start_time.isoformat())

  #---------------------------------------------------------------------------
  @models.permalink
  def get_absolute_url(self):
    return ('swingtime-occurrence', [str(self.event.id), str(self.id)])

  #---------------------------------------------------------------------------
  def __cmp__(self, other):
    return cmp(self.start_time, other.start_time)

  #---------------------------------------------------------------------------
  @property
  def title(self):
    return self.event.title


#-------------------------------------------------------------------------------
def create_event(
  title, 
  event_type,
  description='',
  start_time=None,
  end_time=None,
  **rrule_params
):
  '''
  Convenience function to create an ``Event``, optionally create an
  and associated ``Occurrence``s. ``Occurrence`` creation
  rules match those for ``Event.add_occurrences``.

  Returns the newly created ``Event`` instance.

  Parameters

  ``start_time``
    will default to the current hour if ``None``

  ``end_time``
    will default to ``start_time`` plus swingtime_settings.DEFAULT_OCCURRENCE_DURATION
    hour if ``None``

  ``freq``, ``count``, ``rrule_params``
    follow the ``dateutils`` API (see http://labix.org/python-dateutil)

  '''
  from swingtime.conf import settings as swingtime_settings
  
  if isinstance(event_type, tuple):
          event_type, created = EventType.objects.get_or_create(
              abbr=event_type[0],
              label=event_type[1]
          )

  event = Event.objects.create(
    title=title,
    description=description,
    event_type=event_type
  )

  start_time = start_time or datetime.now().replace(
    minute=0,
    second=0,
    microsecond=0
  )

  end_time = end_time or start_time + swingtime_settings.DEFAULT_OCCURRENCE_DURATION
  event.add_occurrences(start_time, end_time, **rrule_params)
  return event
