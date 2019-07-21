from django import forms
from agenda.models import Event, EventGuest, Invitation, Circle, Contact, Post, Comment
from django.utils.translation import ugettext_lazy as _
from students.models import (
    User
)

class EventForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    date = forms.DateField(label=_('Event date'), widget=forms.SelectDateWidget(attrs={'class': 'date'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

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
        self.user = kwargs.pop('user')
        super(EventGuestForm, self).__init__(*args, **kwargs)
        self.fields['event'].widget = forms.HiddenInput()

        if 'event' in self.initial:
            guests = [user.pk for user in self.initial['event'].guests.all()]
            self.fields['guest'].queryset=User.objects.exclude(pk__in=guests)
            contacts = [contact.user.pk for contact in Contact.objects.filter(owner=self.user)]
            self.fields['guest'].queryset=User.objects.filter(pk__in=contacts)


class InvitationForm(forms.ModelForm):

    class Meta:
        model = Invitation
        fields = ('email',)
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

    status = forms.ChoiceField(choices=(
        (2, 'Desisted'),
        (3, 'Confirmed')
        ))


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    to = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control'}))


class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body',)


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    header = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    status = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-control'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Post
        fields = ('title', 'header', 'body', 'status', 'tags',)
