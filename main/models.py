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
        # constraints = [
        #     models.CheckConstraint(
        #         check=models.Q(wood__lt=1000000),
        #         name='wood__lt=1000000'
        #     ),
        #     models.CheckConstraint(
        #         check=models.Q(stones__lt=1000000),
        #         name='stones__lt=1000000'
        #     ),
        #     models.CheckConstraint(
        #         check=models.Q(iron__lt=1000000),
        #         name='iron__lt=1000000'
        #     ),
        #     models.CheckConstraint(
        #         check=models.Q(food__lt=1000000),
        #         name='food__lt=1000000'
        #     ),
        # ]

    def get_absolute_url(self):
        return reverse_lazy("castle", kwargs={"castle_id": self.pk})

    def __str__(self):
        return self.name


class MilitaryBuildings(models.Model):
    """Модель военных зданий замка пользователя"""

    name = models.CharField(max_length=25, verbose_name="Название здания")
    level = models.PositiveSmallIntegerField(default=1, verbose_name="Уровень здания")
    call_time = models.TimeField(verbose_name="время призыва")
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
    characteristic = models.PositiveSmallIntegerField(
        default=5000, verbose_name="Харакатеристика"
    )
    castle = models.ForeignKey(
        to=Castle, blank=True, null=True, on_delete=models.PROTECT, verbose_name="Замок"
    )

    class Meta:
        ordering = ["name"]
        db_table = "buildings"
        verbose_name = "Здание"
        verbose_name_plural = "Здания"

    def __str__(self):
        return self.name


class ResourceBuildings(models.Model):
    """Модель ресурсо добывающих зданий замка пользователя"""

    name = models.CharField(max_length=25, verbose_name="Название здания")
    level = models.PositiveSmallIntegerField(default=1, verbose_name="Уровень здания")
    production_per_hour = models.PositiveSmallIntegerField(default=500)
    castle = models.ForeignKey(
        to=Castle, blank=True, null=True, on_delete=models.PROTECT, verbose_name="Замок"
    )
    resource = models.CharField(
        max_length=25, verbose_name="Ресурс который производит здание"
    )

    class Meta:
        ordering = ["name"]
        db_table = "resource_buildings"
        verbose_name = "Ресурсное здание"
        verbose_name_plural = "Ресурсные здания"

    def __str__(self):
        return self.name
