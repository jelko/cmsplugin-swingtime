# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from models import *
from django.template import RequestContext
from datetime import datetime, date, timedelta

def eventView(request, event_id):
        event = get_object_or_404(Event, pk=event_id, published=True)
        return render(request, "eventView.html", {'event': event})

def eventIndexView(request):
        occurrences = Occurrence.objects.filter(start_time__gte=datetime.now()).order_by('start_time')
        occurrences = returnPublishedOccurrenceList(occurrences)
        return render(request, "eventIndexView.html", {'occurrences': occurrences})

def eventArchiveView(request):
        occurrences = Occurrence.objects.filter(start_time__lt=datetime.now()).order_by('-start_time')
        occurrences = returnPublishedOccurrenceList(occurrences)
        return render(request, "eventIndexView.html", {'occurrences': occurrences, 'archive': True})

def returnPublishedOccurrenceList(occurrences):
        upcoming_occurrences = []
        for occurrence in occurrences:
            if occurrence.event.published:
                upcoming_occurrences.append(occurrence)
        return upcoming_occurrences

