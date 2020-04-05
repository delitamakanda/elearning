import time

from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger

from django.core import management

logger = get_task_logger(__name__)

@shared_task
def task_example(task_type):
    time.sleep(int(task_type) * 10)
    return True


@task()
def user_email_reminder():
	try:
		"""
		envoie un email aux users ne s'étant pas connecté depuis 2 semaines
		"""
		management.call_command("enroll_reminder", "20", verbosity=0)
	except:
		print("error")
