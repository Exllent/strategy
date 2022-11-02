import pytest
from django.utils import timezone


@pytest.mark.parametrize("field_name, attribute, result", [
    ("name", "blank", True),
    ("name", "max_length", 25),
    ("name", "verbose_name", "Название армии"),
    ("warrior", "null", True),
    ("warrior", "verbose_name", "Воин"), ])
def test_army(field_name, attribute, result, army_model):
    assert getattr(army_model._meta.get_field(field_name), attribute) == result


@pytest.mark.parametrize("attribute, result", [
    ("verbose_name", "Армия"),
    ("verbose_name_plural", "Армии"),
    ("db_table", "army"), ])
def test_army_meta(attribute, result, army_model):
    assert getattr(army_model._meta, attribute) == result


@pytest.mark.parametrize("field_name, attribute, result", [
    ("login", "max_length", 150), ("login", "unique", True),
    ("login", "verbose_name", "Логин"),
    ("nickname", "max_length", 150), ("nickname", "unique", True),
    ("nickname", "verbose_name", "Имя игрока"),
    ("nickname", "blank", True), ("email", "blank", True),
    ("email", "verbose_name", "E-mail"), ("email", "unique", True),
    ("is_staff", "default", False), ("is_staff", "verbose_name", "Статус персонала"),
    ("is_active", "default", True), ("is_active", "verbose_name", "Активность"),
    ("is_registered", "default", False),
    ("is_registered", "verbose_name", "Статус регистрации"),
    ("date_joined", "default", timezone.now),
    ("date_joined", "verbose_name", "Последний вход"),
    ("slug", "max_length", 25), ("slug", "verbose_name", "Слаг"),
    ("slug", "unique", True), ("slug", "blank", True), ("army", "null", True),
    ("army", "blank", True), ("army", "verbose_name", "Армия"), ("race", "null", True),
    ("race", "blank", True), ("race", "verbose_name", "Раса"),
    ("castle", "null", True), ("castle", "blank", True),
    ("castle", "verbose_name", "замок"), ("silver_money", "verbose_name", "Серебро"),
    ("silver_money", "default", 0), ("gold_money", "verbose_name", "Золото"),
    ("gold_money", "default", 0)])
def test_custom_user(field_name, attribute, result, django_user_model):
    assert result == getattr(django_user_model._meta.get_field(field_name), attribute)


@pytest.mark.parametrize("attribute, result", [
    ("verbose_name", "Пользователь"),
    ("verbose_name_plural", "Пользователи"),
    ("db_table", "custom_user")
])
def test_custom_user_meta(attribute, result, django_user_model):
    assert getattr(django_user_model._meta, attribute) == result


@pytest.mark.parametrize("field_name, result", [
    ("silver_money", 1_000_000),
    ("gold_money", 50_000),
])
def test_validators(django_user_model, field_name, result):
    assert django_user_model._meta.get_field(field_name).validators[-1].limit_value == result
