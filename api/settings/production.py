from .common import *

import os

STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')
STATIC_URL = '/static/'

if os.environ.get('EMERGENCY_DEBUG', 'false') == 'true':
    DEBUG = True
    TEMPLATE_DEBUG = True
    INSTALLED_APPS += ('debug_toolbar.apps.DebugToolbarConfig',)
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK':
        'api.settings.production.show_toolbar_callback'
    }


def show_toolbar_callback(request):
    return DEBUG is True
