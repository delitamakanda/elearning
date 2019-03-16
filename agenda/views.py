from django.shortcuts import render, HttpResponseRedirect
from django.forms import HiddenInput
from agenda.models import Event
from agenda.models import EventGuest
from agenda.forms import EventForm, EventGuestForm
from students.models import User

# Create your views here.
def liste_events(request):
    events = Event.objects.all()
    return render(request, 'event/liste.html', {'events': events})

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
            return HttpResponseRedirect('/calendar/%s/detail/' % id)
    else:
        form = EventGuestForm(initial={'event': event})
        guests = [user.pk for user in event.guests.all()]
        form.fields['guest'].queryset=User.objects.exclude(pk__in=guests)
        form.fields['event'].widget = HiddenInput()
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
