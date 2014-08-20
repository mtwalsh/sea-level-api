from .common import *

import getpass
from os.path import join as pjoin

if SECRET_KEY is None:
    SECRET_KEY = 'insecure-secret-key-only-for-development'

if 'true' == os.environ.get('DEBUG', 'true'):  # default on but allow disabling
    DEBUG = TEMPLATE_DEBUG = True  # SECURITY WARNING: insecure! leaks secrets.

if DATABASES is None:
    my_username = getpass.getuser()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': my_username,
        }
    }

INSTALLED_APPS += (
    'debug_toolbar.apps.DebugToolbarConfig',
)

LOG_DIR = pjoin(BASE_DIR, '..', 'log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': ("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s]"
                       " %(message)s"),
            'datefmt': "%d-%b-%y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': pjoin(LOG_DIR, 'django.log'),
            'maxBytes': 4 * 1024 * 1024,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'database_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': pjoin(LOG_DIR, 'database_queries.log'),
            'maxBytes': 4 * 1024 * 1024,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,  # also handle in parent handler
        },

        'django.db.backends': {
            'handlers': ['database_log'],
            'level': 'DEBUG',
            'propagate': False,
        },

        'api.apps': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'api.libs': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
