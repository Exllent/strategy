from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager

from main.models import Castle
from race.models import Race

if TYPE_CHECKING:
    from user.models import CustomUser


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер для создания user и superuser"""

    def create_user(self, login: str, password: str, **extra_fields) -> CustomUser:
        """Метод создаёт пользователя из словаря обработанной формы
        возращает пользователя для авторизации на сайте"""
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, login, password, **extra_fields) -> CustomUser:
        """создаёт superuser с автозаполняемым e-mail по логину"""
        castle = Castle.objects.create(name="Los Angeles")
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("castle_id", castle.pk)
        extra_fields.setdefault("email", f"{login}@gmail.com")
        if Race.get_quantity() != 4:
            Race.create_race()
        return self.create_user(login, password, **extra_fields)
