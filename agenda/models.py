from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from taggit.managers import TaggableManager
from django.utils.text import slugify

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True, null=True)
    guests = models.ManyToManyField(settings.AUTH_USER_MODEL, through='EventGuest')
    date = models.DateTimeField()
    location = models.TextField()
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_event', kwargs=({'pk': self.pk}))

    def delete_url(self):
        return "/calendar/%s/delete/" % self.id


class EventGuest(models.Model):
    status_choices = (
        (0, _('Host')),
        (1, _('Guest')),
        (2, _('Desisted')),
        (3, _('Confirmed')),
    )
    event = models.ForeignKey(Event)
    guest = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.IntegerField(choices=status_choices)

    class Meta:
        unique_together = ('event', 'guest')

    def __str__(self):
        return self.guest.username

    def delete_url(self):
        return "/calendar/%i/guest/%i/delete/" % (self.event.id, self.guest.id)


# Share Application settings.AUTH_USER_MODEL

class Circle(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def contacts(self):
        return self.userinfo_set.all()

    def is_in_circle(self, user):
        if user in self.user_info.contact_set.all():
            return True
        return False

    def get_absolute_url(self):
        return reverse('circle_detail', kwargs=({'pk':self.pk}))

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    circle = models.ManyToManyField(Circle, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('contact_detail', kwargs=({'pk':self.contact.pk}))


class Contact(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friend')
    invitation_send = models.BooleanField()
    invitation_accepted = models.BooleanField()
    optional_informations = models.OneToOneField(UserInfo, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)
        if self.optional_informations == None:
            infos = UserInfo.objects.create()
            self.optional_informations = infos
            self.save()
            infos.save()

    def delete(self, *args, **kwargs):
        optional_informations = self.optional_informations
        super(Contact, self).delete(*args, **kwargs)
        optional_informations.delete()

    def all_contacts(self, user):
        return Contact.objects.filter(owner=user)

    def all_circles(self, user):
        return Circle.objects.filter(owner=user)

    def get_absolute_url(self):
        return reverse('contact_detail', kwargs=({'pk':self.pk}))

    def __str__(self):
        return self.user.username


class Invitation(models.Model):
    email = models.EmailField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        unique_together = ('email', 'sender')

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('invitation_list')
