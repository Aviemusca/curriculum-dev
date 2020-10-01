"""
Django development settings for LO_analysis_project.
Requires environment variable to not be set to 'production'
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# collectstatic files directory
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

# Fixtures settings

FIXTURE_DIRS = [
        ]


# Celery settings

CELERY_BROKER_URL = 'amqp://'
CELERY_BROKER_POOL_LIMIT = None
CELERY_BROKER_CONNECTION_TIMEOUT = 10
CELERYD_CONCURRENCY = 4
CELERY_RESULT_BACKEND = 'django-db'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TIMEZONE = 'Europe/London'
CELERY_ENABLE_UTC = True

