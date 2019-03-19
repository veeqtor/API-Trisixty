release: python manage.py migrate --noinput
web: gunicorn src.wsgi:application --log-file - --log-level debug --preload
worker: celery worker -A src.celery --loglevel=info --concurrency=4