web: gunicorn myelearning.wsgi:application --preload --workers 1
worker: python3 manage.py enroll_reminder --days=20
