from django.shortcuts import render, HttpResponseRedirect
from agenda.models import Event
from agenda.models import EventGuest
from agenda.forms import EventForm, EventGuestForm
from students.models import User

# Create your views here.
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
            return HttpResponseRedirect('/calendar/%i/detail/' % id)
    else:
        form = EventGuestForm(initial={'event': event})
    return render(request, 'event/detail.html', {'event': event, 'form': form})
