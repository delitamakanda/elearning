from django.conf import settings
from django.core.management.base import BaseCommand
from students.models import User, Profile

class Command(BaseCommand):
    help = 'add a profile to each user already created'

    def handle(self, *args, **options):
        users = User.objects.all()
        for u in users:
            Profile.objects.get_or_create(user=u)

            self.stdout.write(self.style.SUCCESS('Created {} Profile'.format(u.username)))