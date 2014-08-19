# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from models import *
from django.template import RequestContext
from datetime import datetime, date, timedelta

def eventView(request, event_type, event_id):
        event = get_object_or_404(Event, pk=event_id, published=True)
        return render(request, "eventView.html", {'event': event})

def eventIndexView(request):
        occurrences = Occurrence.objects.filter(start_time__gte=datetime.now()).order_by('start_time')
        occurrences = returnPublishedOccurrenceList(occurrences)
        return render(request, "eventIndexView.html", {'occurrences': occurrences})
        
def eventTypeView(request, event_type):
        occurrences = Occurrence.objects.filter(start_time__gte=datetime.now()).order_by('start_time')
        try:
                type = EventType.objects.filter(abbr=event_type)[0]
                occurrences.filter(event__event_type=type)
        except:
                return redirect("swingtime-index")
            
        occurrences = returnPublishedOccurrenceList(occurrences)
        return render(request, "eventIndexView.html", {'occurrences': occurrences, 'type':type})

def eventArchiveView(request):
        occurrences = Occurrence.objects.filter(start_time__lt=datetime.now()).order_by('-start_time')
        occurrences = returnPublishedOccurrenceList(occurrences)
        return render(request, "eventIndexView.html", {'occurrences': occurrences, 'archive': True})

def returnPublishedOccurrenceList(occurrences):
        return occurrences.filter(event__published=True)

