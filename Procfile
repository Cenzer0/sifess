web: gunicorn sifess.wsgi --log-file -
worker: celery -A sifess worker -l info
beat: celery -A sifess beat -l info
