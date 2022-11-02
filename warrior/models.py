from django.db import models
from race.models import Race
from user.services import auto_slug
from django.core.validators import MaxValueValidator as Max


class Warrior(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Имя',
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Слаг',
        unique=True,
        blank=True
    )
    health = models.PositiveSmallIntegerField(default=0, verbose_name='Здоровье')
    damage = models.PositiveSmallIntegerField(default=0, verbose_name='Урон')
    armor = models.PositiveSmallIntegerField(default=0, verbose_name='Броня')
    speed = models.PositiveSmallIntegerField(default=0, verbose_name='Скорость')
    quantity = models.PositiveIntegerField(default=0, validators=[Max(limit_value=1_000_000)], verbose_name='Кол-во воинов')
    race = models.ForeignKey(
        to=Race,
        on_delete=models.PROTECT,
        verbose_name='Раса'
    )

    class Meta:
        ordering = ['name']
        db_table = 'characteristic_army'
        verbose_name = "Характеристика-армии"
        verbose_name_plural = "Характеристики-армий"
        # constraints = [
        #     models.CheckConstraint(
        #         check=models.Q(quantity__lte=1000000),
        #         name='quantity__lte=1000000')]

    def save(self, *args, **kwargs):
        self.slug = auto_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
