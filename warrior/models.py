from django.db import models

from race.models import Race
from user.services import auto_slug


class Warrior(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя", unique=True)
    slug = models.SlugField(max_length=50, verbose_name="Слаг", unique=True, blank=True)
    health = models.PositiveSmallIntegerField(default=0, verbose_name="Здоровье")
    damage = models.PositiveSmallIntegerField(default=0, verbose_name="Урон")
    armor = models.PositiveSmallIntegerField(default=0, verbose_name="Броня")
    speed = models.PositiveSmallIntegerField(default=0, verbose_name="Скорость")
    race = models.ForeignKey(to=Race, on_delete=models.PROTECT, verbose_name="Раса")

    class Meta:
        ordering = ["name"]
        db_table = "warrior"
        verbose_name = "Характеристика-армии"
        verbose_name_plural = "Характеристики-армий"

    def save(self, *args, **kwargs):
        self.slug = auto_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_count(cls) -> None:
        return cls.objects.count()

    @classmethod
    def create(
        cls, name: str, health: int, damage: int, armor: int, speed: int, race: int
    ) -> None:
        cls.objects.create(
            name=name,
            health=health,
            damage=damage,
            armor=armor,
            speed=speed,
            race_id=race,
        )
