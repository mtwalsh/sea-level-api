"""
Django settings for sea-level api, common to all environments.

The policy here is that if a setting is truly environment-specific, such
as DEBUG, we should set it to the most secure option here, and let other
environments override. Sometimes the most secure is not to include it,
like SECRET_KEY

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from os.path import abspath, dirname, join as pjoin
from urlparse import urlparse


BASE_DIR = abspath(pjoin(dirname(__file__), '..'))

sys.path.append(pjoin(BASE_DIR, 'apps'))
sys.path.append(pjoin(BASE_DIR, 'libs'))

SECRET_KEY = os.environ.get('SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    'api.sealevelresearch.com',
    'api-staging.sealevelresearch.com',
    'sea-level-api.herokuapp.com',
    'sea-level-api-staging.herokuapp.com',
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'api.apps.predictions',
    'api.apps.locations',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'api.urls'

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# eg postgres://user3123:pass123@database.foo.com:6212/db982398

if 'DATABASE_URL' in os.environ:
    DATABASE_URL = urlparse(os.environ['DATABASE_URL'])
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DATABASE_URL.path[1:],
            'USER': DATABASE_URL.username,
            'PASSWORD': DATABASE_URL.password,
            'HOST': DATABASE_URL.hostname,
            'PORT': DATABASE_URL.port,
        }
    }
else:
    DATABASES = None

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ]
}

# Cross-origin Resource Sharing (CORS)
# See https://github.com/ottoyiu/django-cors-headers/ and
#     http://www.html5rocks.com/en/tutorials/cors/

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS',
)

CORS_ALLOW_CREDENTIALS = False

CORS_PREFLIGHT_MAX_AGE = 3 * 3600
