from myelearning.settings import *
import dj_database_url

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = config('DEBUG')

# email admin

SERVER_EMAIL = config('ADMIN_EMAIL')

ADMINS = [
  (config('ADMIN_NAME'), config('ADMIN_EMAIL')),
]

ALLOWED_HOSTS = ['.herokuapp.com']

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Configure for SSL

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True

# Configure Redis for caching results
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "myelearning"
    }
}
