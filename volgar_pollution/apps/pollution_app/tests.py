from django.test import TestCase

from pollution_app.models import Impurity, ImpurityData
from pollution_app.services.requests_pogodasv import (
    get_impurities_data, write_impurities_data, new_data_point)

class TestClassModelsCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
        test_impurities_dict = {
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
        pass
        for impurity_id, dict_value in test_impurities_dict.items():
            impurity_obj = Impurity(
                impurity_id=int(impurity_id),
                impurity_name=dict_value["name"],
                conlimit=float(dict_value["conlimit"]),
                dangerclass=int(dict_value["dangerclass"]) if dict_value["dangerclass"] != "null" else 0
                )
            impurity_obj.save()

    def test_test(self):
        self.assertTrue(True)

    def test_get_impurities_data(self):
        dict1 = get_impurities_data()
        response_ids = set(('9', '10', '11', '12', '13', '14', '15', '1002', 
                            '1003', '21', '22', '23', '25', '27', '20'))
        msg = 'Не все ожидаемые impurities_id есть в ответе от сервера. Изменился ответ от сервера pogoda-sv?'
        self.assertTrue(response_ids.issubset(dict1.keys()), msg=msg)

    def test_write_impurities_data(self):
        dict1 = {'9': 0.2, '10': 0.045, '11': 0.0, '12': 0.021, '13': 0.0008,
                 '14': 0.2, '15': 0.0, '1002': 1.422, '1003': 0.0, '21': 0.003,
                 '22': 0.0, '23': 0.0, '25': 0.0, '27': 0.0, '20': 0.0}
        write_impurities_data(dict1)
        obj = ImpurityData.objects.get(impurity__impurity_id=9)
        self.assertEqual(obj.value_st, 0.2)
        self.assertEqual(obj.value_pdk, 50)

    def test_new_data_point(self):
        try:
            new_data_point()
            obj = ImpurityData.objects.get(impurity__impurity_id=9)
            self.assertTrue(0 <= obj.value_pdk < 10_000)
        except Exception:
            self.assertTrue(False, msg="Не удалось получить и записать точки с сервера pogoda-sv")




