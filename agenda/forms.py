from django import forms
from agenda.models import Event, EventGuest, Invitation, Circle, Contact
from django.utils.translation import ugettext_lazy as _
from students.models import (
    User
)


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'description', 'date', 'location',)
        exclude = ('guests',)


class EventGuestForm(forms.ModelForm):

    class Meta:
        model = EventGuest
        fields = ('event', 'guest',)
        exclude = ('status',)

    def __init__(self, *args, **kwargs):
        super(EventGuestForm, self).__init__(*args, **kwargs)
        self.fields['event'].widget = forms.HiddenInput()

        if 'event' in self.initial:
            guests = [user.pk for user in self.initial['event'].guests.all()]
            self.fields['guest'].queryset=User.objects.exclude(pk__in=guests)


class InvitationForm(forms.ModelForm):

    class Meta:
        model = Invitation
        fields = ('email', 'sender',)
        exclude = ('sender',)


class CircleForm(forms.ModelForm):

    class Meta:
        model = Circle
        fields = ('name',)
        exclude = ('owner',)


class UpdateGuestForm(forms.ModelForm):

    class Meta:
        model = EventGuest
        fields = ('status',)
        exclude = ('event', 'guest',)

    status = forms.ChoiceField(choices=((2, _('Desisted'), (3, ('Confirmed')))))
