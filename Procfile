web: gunicorn myelearning.wsgi:application --preload
worker: celery -A myelearning worker --loglevel=info -B
release: python3 manage.py migrate
