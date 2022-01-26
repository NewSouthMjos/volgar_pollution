from django.apps import AppConfig


class PollutionAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pollution_app'

    def ready(self):
        from pollution_app.services import data_update
        data_update.start()
