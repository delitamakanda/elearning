from datetime import datetime, timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from courses.models import Course

class Command(BaseCommand):
	help = 'Clears courses older than 365 days from today'

	def add_arguments(self, parser):
		parser.add_argument('duration')

	def handle(self, *args, **options):
		if options['duration'] == 'month':
			number_of_days = 30
		elif options['duration'] == '3month':
			number_of_days = 90
		elif options['duration'] == '6month':
			number_of_days = 180
		elif options['duration'] == '1year':
			number_of_days = 365
		else:
			number_of_days = 30

		self.stdout.write(self.style.SUCCESS('Number of days to delete "%s"' % number_of_days))

		today = timezone.now()
		past_date = today - timedelta(days=number_of_days);

		# this ensures we don't bother running through already marked true
		# objects as deleted.
		to_delete = Course.objects.filter(created__lte=past_date)

		for item in to_delete:
			item.delete()

		self.stdout.write(self.style.SUCCESS('Removed "%s"' % to_delete))