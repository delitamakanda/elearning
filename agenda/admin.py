from django.contrib import admin
from agenda.models import Event
from agenda.models import EventGuest

# Register your models here.
admin.site.register(Event)
admin.site.register(EventGuest)
