from django import forms
from agenda.models import Event, EventGuest
from students.models import (
    User
)


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'description', 'date', 'location',)


class EventGuestForm(forms.ModelForm):

    class Meta:
        model = EventGuest
        fields = ('event', 'guest', 'status',)
