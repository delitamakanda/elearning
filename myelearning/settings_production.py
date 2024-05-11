from myelearning.settings import *
import dj_database_url

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = config('DEBUG', cast=bool)

# email admin

SERVER_EMAIL = config('ADMIN_EMAIL')

ADMINS = [
  (config('ADMIN_NAME'), config('ADMIN_EMAIL')),
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('SENDGRID_SERVER')
EMAIL_PORT = config('SENDGRID_PORT')
EMAIL_HOST_USER = config('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = config('SENDGRID_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 500

ALLOWED_HOSTS = ['*',]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configure for SSL

# SECURE_SSL_REDIRECT = True
# CSRF_COOKIE_SECURE = True

SESSION_EXPIRE_SECONDS = 18000  # 5 hours

# Configure Redis for caching results
CACHE_MIDDLEWARE_SECONDS = 60 * 10  # 10 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'myelearning'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("HEROKU_REDIS_AQUA_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "MAX_ENTRIES": 1000,
        },
        "KEY_PREFIX": "myelearning",
        "TIMEOUT": 300
    }
}

# Media storages

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

DEFAULT_FILE_STORAGE = 'myelearning.storage_backends.MediaStorage'

# Task async
CELERY_BROKER_URL = config('HEROKU_REDIS_AQUA_URL')
CELERY_RESULT_BACKEND = config('HEROKU_REDIS_AQUA_URL')

