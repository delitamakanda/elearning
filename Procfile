web: gunicorn myelearning.wsgi:application --preload
worker: celery worker --app=myelearning --loglevel=info -B
release: python3 manage.py migrate
