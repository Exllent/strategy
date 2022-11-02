from django.db import models

from race.constants import RaceChoices


class Race(models.Model):
    """Модель доступных рас всей игры"""

    name = models.CharField(
        max_length=25,
        choices=RaceChoices.choices,
        verbose_name="Раса"
    )

    class Meta:
        ordering = ['name']
        db_table = "race"
        verbose_name = "Раса"
        verbose_name_plural = "Расы"

    def __str__(self):
        return self.name

    @staticmethod
    def get_race():
        race_list = [(i.id, i.name) for i in Race.objects.all()]
        return race_list
