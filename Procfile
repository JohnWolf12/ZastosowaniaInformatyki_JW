release: python manage.py migrate
web: gunicorn webApplication.wsgi --log-file -
python manage.py collectstatic --noinput