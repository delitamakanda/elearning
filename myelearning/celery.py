import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myelearning.settings')

app = Celery('myelearning')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'user_email_reminder_every_week': {
        'task': 'courses.tasks.user_email_reminder',
		'schedule': crontab(hour=7, minute=30, day_of_week=1),
		'args': ()
    }
}

app.conf.timezone = 'UTC'
