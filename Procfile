web: gunicorn --env DJANGO_SETTINGS_MODULE=myelearning.settings_production myelearning.wsgi
worker: python3 manage.py enroll_reminder --days=20
