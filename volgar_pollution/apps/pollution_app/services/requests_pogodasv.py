from multiprocessing.sharedctypes import Value
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

def check_impurities():
    """
    Запуск при старте: проверяет, что все значения
    расшифровки загрязнений в таблице БД, и если нет,
    добавляет отсутствующие записи. Возвращает добавленные
    записи
    """
    not_in_bd_impurities = _is_initial_impurities_in_bd()
    if len(not_in_bd_impurities) == 0:
        return []
    _write_impurities_initial(not_in_bd_impurities)
    return not_in_bd_impurities

def _write_impurities_initial(impurities_ids: list):
    """
    Записывает расшифровку недостающих загрязнений в БД
    (таблицу Impurity). Принимает недостающие загрязнения
    """

    impurities_dict = {
        "9": {
            "impurity_id": "9",
            "name": "Азота оксид",
            "conlimit": "0.4",
            "dangerclass": "3",
        },
        "10": {
            "impurity_id": "10",
            "name": "Азота диоксид",
            "conlimit": "0.2",
            "dangerclass": "3",
        },
        "11": {
            "impurity_id": "11",
            "name": "Аммиак",
            "conlimit": "0.2",
            "dangerclass": "4",
        },
        "12": {
            "impurity_id": "12",
            "name": "Сера диоксид",
            "conlimit": "0.5",
            "dangerclass": "3",
        },
        "13": {
            "impurity_id": "13",
            "name": "Сероводород",
            "conlimit": "0.008",
            "dangerclass": "2",
        },
        "14": {
            "impurity_id": "14",
            "name": "Углерода оксид",
            "conlimit": "5",
            "dangerclass": "4",
        },
        "15": {
            "impurity_id": "15",
            "name": "Формальдегид",
            "conlimit": "0.05",
            "dangerclass": "null",
        },
        "1002": {
            "impurity_id": "1002",
            "name": "Углеводороды C1-C5",
            "conlimit": "200",
            "dangerclass": "4",
        },
        "1003": {
            "impurity_id": "1003",
            "name": "Углеводороды C6-C10",
            "conlimit": "50",
            "dangerclass": "3",
        },
        "21": {
            "impurity_id": "21",
            "name": "Толуол",
            "conlimit": "0.6",
            "dangerclass": "null",
        },
        "22": {
            "impurity_id": "22",
            "name": "Этилбензол",
            "conlimit": "0.02",
            "dangerclass": "null",
        },
        "23": {
            "impurity_id": "23",
            "name": "Хлорбензол",
            "conlimit": "0.1",
            "dangerclass": "null",
        },
        "25": {
            "impurity_id": "25",
            "name": "О-ксилол",
            "conlimit": "0.3",
            "dangerclass": "null",
        },
        "27": {
            "impurity_id": "27",
            "name": "Фенол",
            "conlimit": "0.01",
            "dangerclass": "null",
        },
        "20": {
            "impurity_id": "20",
            "name": "Бензол",
            "conlimit": "0.3",
            "dangerclass": "null",
        }
    }
    adding_dict = dict()
    for impurity_id in impurities_ids:
        if not(str(impurity_id) in impurities_dict.keys()):
            raise ValueError(f'Переданное значение @{impurity_id} функции не находится в стандартном словаре!')
        adding_dict[str(impurity_id)] = impurities_dict[str(impurity_id)]

    for impurity_id, dict_value in adding_dict.items():
        impurity_obj = Impurity(
            impurity_id=int(impurity_id),
            impurity_name=dict_value["name"],
            conlimit=float(dict_value["conlimit"]),
            dangerclass=int(dict_value["dangerclass"]) if dict_value["dangerclass"] != "null" else 0
            )
        impurity_obj.save()

def _is_initial_impurities_in_bd():
    """
    Проверяет, каких начальных значений (о загрязнении) нет в
    БД (таблице Impurity) и отдаёт список этих значений
    """
    impurities_ids = [
        9, 10, 11, 12, 13, 14, 15, 1002, 1003, 21, 22, 23, 25, 20, 27
    ]
    impurities_not_in_bd = []
    for impurity_id in impurities_ids:
        try:
            Impurity.objects.get(impurity_id=impurity_id)
        except Impurity.DoesNotExist:
            impurities_not_in_bd.append(impurity_id)
    return impurities_not_in_bd

def main():
    a = get_impurities_data()
    print(a)


if __name__ == '__main__':
    main()


