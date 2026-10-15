"""Django settings for myelearning project."""

from pathlib import Path
import sys
from decouple import config
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = BASE_DIR
sys.path.insert(0, str(PROJECT_ROOT))

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', 'dummy_secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', 'True', cast=bool)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'apps.courses.apps.CoursesConfig',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admindocs',
    'crispy_forms',
    'apps.students.apps.StudentsConfig',
    'embed_video',
    'rest_framework',
    'storages',
    'widget_tweaks',
    'corsheaders',
    'taggit',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'apps.students.middleware.SessionTimeoutMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

# if DEBUG == False:
    # MIDDLEWARE += ('courses.middleware.SubdomainCourseMiddleware')


ROOT_URLCONF = 'myelearning.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # template at the root of the project
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myelearning.wsgi.application'

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Custom auth

AUTH_USER_MODEL = 'students.User'
LOGIN_REDIRECT_URL = reverse_lazy('students:classroom')
LOGIN_URL = reverse_lazy('login')
LOGOOUT_URL = reverse_lazy('logout')
LOGOUT_REDIRECT_URL = reverse_lazy('courses:course_list')


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'apps.students.authentication.EmailAuthBackend',
]


# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS = 60 * 15  # 15 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'el'

# DRF
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    )
}

# Mailer
DEFAULT_FROM_EMAIL = config('ADMIN_EMAIL', 'no-reply@myelearnig.com')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Session
SESSION_EXPIRE_SECONDS = 18000  # 5 hours
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

DEVELOPER_KEY = config('DEVELOPER_API_KEY', 'developer_key_here')

# corsheaders
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'https://myelearning.herokuapp.com',
    'http://localhost:8080',
    'http://localhost:8100',
    'http://localhost:8000',
    'http://localhost:3000',
    'https://pwa-myelearning.netlify.app',
    'http://localhost',
]
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
)

# Task async
CELERY_BROKER_URL = config('REDIS_URL', 'redis://localhost:6379/0', cast=str)
CELERY_RESULT_BACKEND = config('REDIS_URL', 'redis://localhost:6379/0', cast=str)

CRISPY_TEMPLATE_PACK = 'bootstrap4'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
