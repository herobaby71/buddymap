web: gunicorn buddymap.wsgi --log-file -
web: daphne buddymap.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2
