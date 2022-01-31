from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class PollutionAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pollution_app'

    def ready(self):
        pass
        # Запуск собрания данных по расписанию
        # from pollution_app.services import data_update
        # data_update.start()

        # Запуск инициализации начальных значений в БД
        # по расшифровке загрязнений, Impurity
        # from pollution_app.services.requests_pogodasv import check_impurities
        # not_in_bd_impurities = check_impurities()
        # logger.info(f'Добавлены данные в таблицу Impurity: {not_in_bd_impurities}')
