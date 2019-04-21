import json
import datetime

from django.shortcuts import render, HttpResponseRedirect, render_to_response
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.generic.list import ListView
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.forms import HiddenInput
from agenda.models import Event
from agenda.models import EventGuest
from agenda.forms import EventForm, EventGuestForm
from students.models import User

# Create your views here.
def liste_events(request):
    events = Event.objects.all()
    paginator = Paginator(events, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        events = paginator.page(page)
    except (EmptyPage, InvalidPage):
        events = paginator.page(paginator.num_pages)
    return render(request, 'event/liste.html', {'events': events})


class ListEvents(ListView):

    def get_queryset(self):
        events = Event.objects.filter(
            guests = self.request.user,
            date__gte = datetime.datetime.now()
        )
        if 'champ' in self.kwargs:
            events = events.filter(
                (self.kwargs['champ'],
                self.kwargs['terme'])
            )
        return events

def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return HttpResponseRedirect('/calendar/%i/detail/' % event.pk)
    else:
        form = EventForm()
    return render(request, 'event/create.html', {'form': form})

def detail_event(request, id):
    event = Event.objects.get(pk=id)
    if request.method == "POST":
        form = EventGuestForm(request.POST)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                delete_form = render_to_string(
                    "partial/delete_form.html",
                    {'delete_url': form.instance.delete_url()}
                )
                data = {
                    'guest': form.instance.guest.username,
                    'get_status_display' : form.instance.get_status_display(),
                    'delete_form': delete_form
                }
                return HttpResponse(
                    json.dumps(data),
                    content_type="application/json"
                )
            return HttpResponseRedirect('/calendar/%s/detail/' % id)
    else:
        form = EventGuestForm(initial={'event': event})
        guests = [user.pk for user in event.guests.all()]
        form.fields['guest'].queryset=User.objects.exclude(pk__in=guests)
        form.fields['event'].widget = HiddenInput()
    if request.is_ajax():
        render_to_response(
            'partial/guest_form.html',
            { 'event': event, 'form': form}
        )
    return render(request, 'event/detail.html', {'event': event, 'form': form})

def delete_guest(request, id, guest):
    if request.method == "POST":
        event = Event.objects.get(pk=id)
        guest = User.objects.get(pk=guest)
        to_delete = EventGuest.objects.get(
            event = event,
            guest = guest
        )
        to_delete.delete()
        if request.is_ajax():
            return HttpResponse('OK')
    return HttpResponseRedirect('/calendar/%s/detail/' % id)


def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(pk = id)
        event.delete()
    return HttpResponseRedirect('/calendar/liste/')

def update_event(request, id):
    event = Event.objects.get(pk = id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            u = form.save()
            return HttpResponseRedirect('/calendar/%i/detail/' % u.pk)
    else:
        form = EventForm(instance = event)
    return render(request, 'event/create.html', {'form': form})
