"""
Django production settings for LO_analysis_project Heroku deployment.
Requires environment variable to be set to 'production'
"""
from .base import *

import django_heroku

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Heroku collectstatic files default
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Fixtures settings

FIXTURE_DIRS = [
        ]



# Celery settings
CELERY_BROKER_URL = os.environ.get('CLOUDAMQP_URL')
BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_TIMEOUT = 10
CELERYD_CONCURRENCY = 4
CELERY_RESULT_BACKEND = 'django-db'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TIMEZONE = 'Europe/London'
CELERY_ENABLE_UTC = True


django_heroku.settings(locals())
