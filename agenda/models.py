from django.db import models
from django.utils.translation import ugettext_lazy as _
from students.models import User

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    guests = models.ManyToManyField(User, through='EventGuest')
    date = models.DateTimeField()
    location = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/calendar/%s/detail/" % self.id

    def delete_url(self):
        return "/calendar/%s/delete/" % self.id


class EventGuest(models.Model):
    status_choices = (
        (0, _('Host')),
        (1, _('Guest')),
        (2, _('Desisted')),
    )
    event = models.ForeignKey(Event)
    guest = models.ForeignKey(User)
    status = models.IntegerField(choices=status_choices)

    class Meta:
        unique_together = ('event', 'guest')

    def __str__(self):
        return '{} - {}'.format(self.event, self.guest)

    def delete_url(self):
        return "/calendar/%i/guest/%i/delete/" % (self.event.id, self.guest.id)
