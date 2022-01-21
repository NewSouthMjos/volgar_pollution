import requests

def get_impurities():
    """
    Получает данные по загрязнению с сервера pogoda-sv.ru
    Возвращает словарь impurity_id:значение загрязнения
    """
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
        value = impurity_json['value']
        impurity_id = impurity_json['impurity_id']
        # print(impurity_id, value)
        result_dict[impurity_id] = value
    return result_dict

def main():
    a = get_impurities()
    print(a)


if __name__ == '__main__':
    main()


