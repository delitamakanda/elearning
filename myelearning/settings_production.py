from .settings import *

DEBUG = config('DEBUG')

ADMINS = (
  ('Delita Makanda', 'delita.makanda@gmail.com'),
)

ALLOWED_HOSTS = ['.herokuapp.com']

# Configure for SSL
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
