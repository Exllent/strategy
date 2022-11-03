from django.db import models

from race.constants import RaceChoices


class Race(models.Model):
    """Модель доступных рас всей игры"""

    name = models.CharField(
        max_length=25,
        choices=RaceChoices.choices,
        verbose_name="Раса"
    )

    def __str__(self):
        return self.name

    @classmethod
    def create_race(cls):
        for i in RaceChoices.choices:
            cls.objects.create(name=i[-1]).save()

    @classmethod
    def get_quantity(cls):
        return cls.objects.all().count()

    class Meta:
        ordering = ['name']
        db_table = "race"
        verbose_name = "Раса"
        verbose_name_plural = "Расы"
