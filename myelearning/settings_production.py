from myelearning.settings import *
import dj_database_url

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = config('DEBUG')

ADMINS = (
  ('Delita Makanda', 'delita.makanda@gmail.com'),
)

ALLOWED_HOSTS = ['.herokuapp.com']

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Configure for SSL
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
