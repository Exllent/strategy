import pytest


@pytest.mark.parametrize(
    "field_name, attribute, result",
    [
        ("name", "max_length", 50),
        ("name", "verbose_name", "Имя"),
        ("name", "unique", True),
        ("slug", "unique", True),
        ("slug", "max_length", 50),
        ("slug", "verbose_name", "Слаг"),
        ("slug", "blank", True),
        ("race", "verbose_name", "Раса"),
        ("health", "default", 0),
        ("health", "verbose_name", "Здоровье"),
        ("damage", "default", 0),
        ("damage", "verbose_name", "Урон"),
        ("armor", "default", 0),
        ("armor", "verbose_name", "Броня"),
        ("speed", "default", 0),
        ("speed", "verbose_name", "Скорость"),
        ("quantity", "default", 0),
        ("quantity", "verbose_name", "Кол-во воинов"),
    ],
)
def test_warrior(field_name, attribute, result, warrior_model):
    assert result == getattr(warrior_model._meta.get_field(field_name), attribute)


@pytest.mark.parametrize(
    "attribute, result",
    [
        ("verbose_name", "Характеристика-армии"),
        ("verbose_name_plural", "Характеристики-армий"),
        ("db_table", "characteristic_army"),
    ],
)
def test_warrior_meta(warrior_model, attribute, result):
    assert getattr(warrior_model._meta, attribute) == result


def test_warrior_validator(warrior_model):
    assert (
        warrior_model._meta.get_field("quantity").validators[-1].limit_value
        == 1_000_000
    )
