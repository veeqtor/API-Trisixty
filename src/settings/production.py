"""Production settings"""

from os import environ
from .base import *

ENV = ('production', 'prod', 'Heroku', 'HEROKU', 'PROD', 'PRODUCTION')

HOST_ENV = environ.get('HOST_ENV')

if HOST_ENV in ENV:

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    CACHES = {
        "default": {
             "BACKEND": "redis_cache.RedisCache",
             "LOCATION": os.environ.get('REDIS_URL'),
        }
    }

    import django_heroku

    # Activate Django-Heroku.
    django_heroku.settings(locals())
