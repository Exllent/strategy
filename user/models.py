from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import (
    UnicodeUsernameValidator,
    ASCIIUsernameValidator,
)
from django.core.validators import MaxValueValidator as Max
from django.db import models
from django.utils import timezone

from main.models import Castle
from race.models import Race
from user.managers import CustomUserManager
from user.services import auto_slug
from warrior.models import Warrior


class Army(models.Model):
    """Модель Армий игроков"""

    name = models.CharField(max_length=25, blank=True, verbose_name="Название армии")
    warrior = models.ForeignKey(
        to=Warrior, on_delete=models.CASCADE, null=True, verbose_name="Воин"
    )
    quantity = models.PositiveIntegerField(
        default=0, validators=[Max(limit_value=1_000_000)], verbose_name="Кол-во воинов"
    )

    class Meta:
        ordering = ["name"]
        db_table = "army"
        verbose_name = "Армия"
        verbose_name_plural = "Армии"

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя"""

    login_validator = ASCIIUsernameValidator()
    nickname_validator = UnicodeUsernameValidator()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = ()

    login = models.CharField(
        max_length=150,
        unique=True,
        validators=[login_validator],
        error_messages={"unique": "Пользователь с этим логином уже существует"},
        verbose_name="Логин",
    )
    nickname = models.CharField(
        max_length=150,
        validators=[nickname_validator],
        blank=True,
        unique=True,
        error_messages={"unique": "Пользователь с этим nickname уже существует"},
        verbose_name="Имя игрока",
    )
    email = models.EmailField(
        blank=True,
        error_messages={"unique": "Пользователь с этой почтой уже существует"},
        unique=True,
        verbose_name="E-mail",
    )
    is_staff = models.BooleanField(default=False, verbose_name="Статус персонала")
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    is_registered = models.BooleanField(
        default=False, verbose_name="Статус регистрации"
    )
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name="Последний вход"
    )
    slug = models.SlugField(max_length=25, verbose_name="Слаг", unique=True, blank=True)
    army = models.ForeignKey(
        to=Army, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Армия"
    )
    race = models.ForeignKey(
        to=Race, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Раса"
    )
    castle = models.OneToOneField(
        to=Castle, on_delete=models.CASCADE, blank=True, null=True, verbose_name="замок"
    )
    silver_money = models.PositiveBigIntegerField(
        default=0, validators=[Max(limit_value=1_000_000)], verbose_name="Серебро"
    )
    gold_money = models.PositiveSmallIntegerField(
        default=0, validators=[Max(limit_value=50_000)], verbose_name="Золото"
    )

    objects = CustomUserManager()

    class Meta:
        ordering = ["login"]
        db_table = "custom_user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.login
        self.slug = auto_slug(self.nickname)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nickname
