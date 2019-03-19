"""Test settings"""

from os import environ
from .base import *

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': environ.get('DB_HOST'),
        'NAME': environ.get('TEST_DB_NAME'),
        'USER': environ.get('DB_USER'),
        'PASSWORD': environ.get('DB_PASS'),
    }
}

# Email backends
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


# Celery related
CELERY_ALWAYS_EAGER = True
