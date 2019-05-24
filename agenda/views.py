import json
import datetime

from django.contrib.sites.models import Site
from django.shortcuts import render, HttpResponseRedirect, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.forms.utils import ErrorList
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from django.forms import HiddenInput
from agenda.models import Event
from agenda.models import EventGuest
from agenda.forms import EventForm, EventGuestForm, InvitationForm
from students.models import User

from agenda.models import Circle
from agenda.models import Contact
from agenda.models import Invitation
from agenda.models import UserInfo

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


class DetailEvents(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(DetailEvents, self).get_context_data(**kwargs)
        form = EventGuestForm(initial={'event': self.object})
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = EventGuestForm(self.request.POST)
        if form.is_valid():
            form.save()
            if self.request.is_ajax():
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
            else:
                return HttpResponseRedirect('/calendar/%s/detail/' % form.instance.event.id)
        else:
            if request.is_ajax():
                return render(request,
                    'partial/guest_form.html',
                    { 'event': form.instance.event, 'form': form}
                )
            else:
                return render(request, 'event/detail.html', {'event': form.instance.event, 'form': form})

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



@method_decorator([login_required], name='dispatch')
class InvitationListView(ListView):

    def get_queryset(self):
        return Invitation.objects.filter(sender=self.request.user)


def send_invitation(invitation):
    try:
        User.objects.get(email=invitation.email)
        message = _('%s vous a ajouté à ses contacts.' % invitation.sender.username)
    except User.DoesNotExist:
        message = _('%s vous invite à rejoindre ses contacts. %s Inscrivez vous sur http://%s/accounts/signup/ pour accepter son invitation.' % invitation.sender.username, Site.objects.get_current().domain)

    send_mail(_('Une invitation a été envoyée'),message,invitation.sender,[invitation.email], fail_silently=False)


@method_decorator([login_required], name='dispatch')
class InvitationCreateView(CreateView):
    form_class = InvitationForm
    model = Invitation

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.sender = self.request.user

        try:
            Invitation.objects.get(email=obj.email, sender=obj.sender)
            form._errors['email'] = ErrorList(
                [_('Une invitation a déja été envoyée à cette adresse.')]
            )
            return super(InvitationCreateView, self).form_invalid(form)
        except Invitation.DoesNotExist:
            pass
        obj.save()
        send_invitation(obj)
        return HttpResponseRedirect(obj.get_absolute_url())
