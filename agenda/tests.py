from django.test import TestCase
from agenda.models import Event, EventGuest
from students.models import User
from datetime import datetime
from datetime import timedelta

# Create your tests here.
class EventGuestTest(TestCase):
    def test_create_user(self):
        guest1 = User(first_name='test', last_name='test')
        guest1.save()
        guest = User.objects.get(first_name='test')
        self.assertEqual(guest.last_name, 'test')

    def test_create_event(self):
        event = Event(name='new event', description='', date=datetime.now(), location='test')
        event.save()
        event = Event.objects.get(name='new event')
        self.assertEqual(event.location, 'test')

    def test_create_event_guest(self):
        self.test_create_user()
        self.test_create_event()
        guest = User.objects.get(first_name='test')
        event = Event.objects.get(name='new event')
        event_guest = EventGuest(
            event=event,
            guest=guest,
            status=1
        )
        event_guest.save()
        evnt = EventGuest.objects.get(event=event,guest=guest)
        self.assertEqual(evnt.status, 1) 

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        1 + 1 = 2
        """
        self.assertEqual(1 + 1, 2)
