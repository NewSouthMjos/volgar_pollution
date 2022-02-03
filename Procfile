release: python manage.py migrate
web: gunicorn volgar_pollution.wsgi --log-file -
clock: python volgar_pollution/apps/pollution_app/services/data_update.py
