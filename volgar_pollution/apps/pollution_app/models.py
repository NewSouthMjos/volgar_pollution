from django.db import models

class Impurity(models.Model):
    """Примеси в воздухе"""
    impurity_id = models.PositiveSmallIntegerField(
        verbose_name='id примеси согласно pogoda-sv.ru'
    )
    impurity_name = models.CharField(verbose_name='имя примеси', max_length=50)
    conlimit = models.FloatField(verbose_name='ПДКм.р.')
    dangerclass = models.PositiveSmallIntegerField(
        verbose_name='класс опасности', null=True, blank=True
    )

class ImpurityData(models.Model):
    """
    Данные по загрязнениям в определенны точки времени.
    Используются для построения графика
    """
    datetime = models.DateTimeField(verbose_name='Дата и время', auto_now_add=True)
    impurity = models.ForeignKey(Impurity, on_delete=models.CASCADE)
    value_st = models.FloatField(verbose_name='Значение в мг/м3')
    value_pdk = models.PositiveSmallIntegerField(
        verbose_name='Значение в процентах от ПДК'
    )

