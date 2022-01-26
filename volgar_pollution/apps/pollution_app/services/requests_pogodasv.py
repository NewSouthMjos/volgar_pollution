import requests
import logging

from pollution_app.models import Impurity, ImpurityData


logger = logging.getLogger(__name__)

def get_impurities_data():
    """
    Получает данные по загрязнению с сервера pogoda-sv.ru
    Возвращает словарь impurity_id:значение загрязнения
    """
    logger.info('Запрос данных с pogoda-sv...')
    url = 'http://pogoda-sv.ru/apps/volgar/controller/frontend.php?action=getData&postId=11'
    request = requests.get(url)
    if request.status_code != 200:
        raise ValueError('Response from server is not OK')
    json_dict = request.json()
    result_dict = dict()
    for impurity in json_dict['response']:
        impurity_json = json_dict['response'][impurity]

        # Datetime с сервера pogoda-sv не важна, у них UTC и отставание на
        # 5 минут
        # dt = impurity_json['time']
        value = float(impurity_json['value'])
        impurity_id = impurity_json['impurity_id']
        # print(impurity_id, value)
        result_dict[impurity_id] = value
    logger.info('Запрос данных с pogoda-sv - успешно!')
    return result_dict

def write_impurities_data(impurities_dict: dict):
    """Записывает данные по загрязнениям в БД"""
    logger.info('Запись данных загрязнения в БД...')
    bd_errors_count = 0
    for impurity_id, value in impurities_dict.items():
        try:
            impurity_obj = Impurity.objects.get(impurity_id=int(impurity_id))
            value_pdk = round(value*100/impurity_obj.conlimit)
            impuritydata_obj = ImpurityData(
                impurity=impurity_obj,
                value_st=value,
                value_pdk=value_pdk)
            impuritydata_obj.save()
        except Impurity.DoesNotExist:
            bd_errors_count += 1
            logger.warning(f'Запись новой точки: impurity_id #{impurity_id} не найден в БД(таблице Impurity)!')
    logger.info(f'Запись данных загрязнения в БД успешно, ошибок: {bd_errors_count}')


def new_data_point():
    """Пытается положить в БД новые данные по загрязнению"""
    impurities_dict = get_impurities_data()
    write_impurities_data(impurities_dict)

def main():
    a = get_impurities_data()
    print(a)


if __name__ == '__main__':
    main()


