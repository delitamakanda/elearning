from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
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
        return reverse('detail_event', kwargs={'pk': self.pk})

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


# Share Application Users

class Circle(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User)

    def contacts(self):
        return self.user_info.contact_set.all()

    def is_in_circle(self, user):
        if user in self.user_info.contact_set.all():
            return True
        return False

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    circle = models.ManyToManyField(Circle)
    notes = models.TextField()

    def __str__(self):
        return self.circle


class Contact(models.Model):
    owner = models.ForeignKey(User)
    user = models.ForeignKey(User, related_name='friend')
    invitation_send = models.BooleanField()
    invitation_accepted = models.BooleanField()
    optional_informations = models.OneToOneField(UserInfo, blank=True, null=True)

    def all_contacts(self, user):
        return Contact.objects.filter(owner=user)

    def all_circles(self, user):
        return Circle.objects.filter(owner=user)

    def __str__(self):
        return self.owner


class Invitation(models.Model):
    email = models.EmailField()
    sender = models.ForeignKey(User)

    class Meta:
        unique_together = ('email', 'sender')

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('invitation_list')
