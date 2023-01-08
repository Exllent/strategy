from django.core.validators import MaxValueValidator as Max
from django.db import models
from django.urls import reverse_lazy


class Castle(models.Model):
    """Модель замка игрока"""

    name = models.CharField(max_length=25, blank=True, verbose_name="Имя")

    wood = models.PositiveSmallIntegerField(
        default=0, validators=[Max(limit_value=1_000_000)], verbose_name="Дерево"
    )
    stones = models.PositiveSmallIntegerField(
        default=0, validators=[Max(limit_value=1_000_000)], verbose_name="Камень"
    )
    iron = models.PositiveSmallIntegerField(
        default=0, validators=[Max(limit_value=1_000_000)], verbose_name="Железо"
    )
    food = models.PositiveSmallIntegerField(
        default=0, validators=[Max(limit_value=1_000_000)], verbose_name="Еда"
    )

    class Meta:
        ordering = ["name"]
        db_table = "castle"
        verbose_name = "Замок"
        verbose_name_plural = "Замки"

    def update_quantity_resources(self, **resources: dict) -> None:
        self.__class__.objects.update(**resources)

    @classmethod
    def get_castle(cls, castle_id: int):
        return cls.objects.get(pk=castle_id)

    def get_absolute_url(self):
        return reverse_lazy("castle", kwargs={"castle_id": self.pk})

    def __str__(self):
        return self.name


class MilitaryBuildings(models.Model):
    """Модель военных зданий замка пользователя"""

    name = models.CharField(max_length=25, verbose_name="Название здания")
    level = models.PositiveSmallIntegerField(default=1, verbose_name="Уровень здания")
    call_time = models.TimeField(verbose_name="время призыва")
    building_price = models.PositiveSmallIntegerField(
        default=3000, verbose_name="Цена здания"
    )
    castle = models.ForeignKey(
        to=Castle, blank=True, null=True, on_delete=models.PROTECT, verbose_name="Замок"
    )

    class Meta:
        ordering = ["name"]
        db_table = "military_buildings"
        verbose_name = "Военное здание"
        verbose_name_plural = "Военные здания"

    def __str__(self):
        return self.name


class Buildings(models.Model):
    """Модель зданий замка пользователя"""

    name = models.CharField(max_length=25, verbose_name="Название здания")
    level = models.PositiveSmallIntegerField(default=1, verbose_name="Уровень здания")
    capacity = models.PositiveSmallIntegerField(
        default=5000, verbose_name="Вместительность"
    )
    building_price = models.PositiveSmallIntegerField(
        default=3000, verbose_name="Цена здания"
    )
    castle = models.ForeignKey(
        to=Castle, blank=True, null=True, on_delete=models.PROTECT, verbose_name="Замок"
    )

    class Meta:
        ordering = ["name"]
        db_table = "buildings"
        verbose_name = "Здание"
        verbose_name_plural = "Здания"

    @classmethod
    def get_capacity_resources_by_castle(cls, castle_id):
        return (
            cls.objects.select_related("castle")
            .only(
                "capacity",
                "castle__food",
                "castle__iron",
                "castle__wood",
                "castle__stones",
            )
            .get(castle_id=castle_id)
        )

    @classmethod
    def get_capacity_stock(cls, castle_id: int):
        return cls.objects.get(castle_id=castle_id, name="Склад").capacity

    def __str__(self):
        return self.name


class ResourceBuildings(models.Model):
    """Модель ресурсов добывающих зданий замка пользователя"""

    name = models.CharField(max_length=25, verbose_name="Название здания")
    level = models.PositiveSmallIntegerField(default=1, verbose_name="Уровень здания")
    production_per_hour = models.PositiveSmallIntegerField(default=500)
    castle = models.ForeignKey(
        to=Castle, blank=True, null=True, on_delete=models.PROTECT, verbose_name="Замок"
    )
    building_price = models.PositiveSmallIntegerField(
        default=3000, verbose_name="Цена здания"
    )
    resource = models.CharField(
        max_length=25, verbose_name="Ресурс который производит здание"
    )

    class Meta:
        ordering = ["name"]
        db_table = "resource_buildings"
        verbose_name = "Ресурсное здание"
        verbose_name_plural = "Ресурсные здания"

    @classmethod
    def get_resources_buildings(cls, castle_id):
        return (
            cls.objects.select_related("castle")
            .only(
                "resource",
                "castle__food",
                "castle__iron",
                "castle__wood",
                "castle__stones",
                "production_per_hour",
            )
            .filter(castle_id=castle_id)
        )

    @classmethod
    def get_production_per_hour(cls, castle_pk: int, resource_name: str):
        return cls.objects.get(
            castle_id=castle_pk, resource=resource_name
        ).production_per_hour

    def __str__(self):
        return self.name
