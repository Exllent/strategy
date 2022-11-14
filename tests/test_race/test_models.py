import pytest

from race.constants import RaceChoices


@pytest.mark.parametrize("field_name, attribute, result", [
    ("name", "max_length", 25),
    ("name", "choices", RaceChoices.choices),
    ("name", "verbose_name", "Раса"),
])
def test_race(race_model, field_name, attribute, result):
    assert getattr(race_model._meta.get_field(field_name), attribute) == result


@pytest.mark.django_db
def test_methods_race(race_model):
    assert race_model.get_quantity() == 0
    race_model.create_race()
    assert race_model.get_quantity() == 4
