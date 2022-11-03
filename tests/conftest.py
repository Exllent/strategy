import pytest
from main.models import Castle
from race.models import Race
from race.constants import RaceChoices
from warrior.models import Warrior
from user.models import Army


@pytest.mark.django_db
@pytest.fixture()
def create_user(django_user_model):
    return django_user_model.objects.create_user(login="login_user",
                                                 password="password_user",
                                                 nickname="nickname_user",
                                                 email="email_user@gmail.com",
                                                 castle_id=1, is_registered=True)


@pytest.mark.django_db
@pytest.fixture()
def create_admin(django_user_model):
    return django_user_model.objects.create_superuser(
        login="login_admin",
        password="password_admin")


@pytest.mark.django_db
@pytest.fixture()
def create_castle():
    castle = Castle.objects.create(name="Los angeles")
    castle.save()


@pytest.mark.django_db
@pytest.fixture()
def get_users(django_user_model):
    return django_user_model.objects.all()


@pytest.mark.django_db
@pytest.fixture()
def create_race():
    for i in RaceChoices.choices:
        Race.objects.create(name=i[-1]).save()


@pytest.mark.django_db
@pytest.fixture()
def get_race():
    def wrapper(name):
        return Race.objects.get(name=name)

    return wrapper


@pytest.mark.django_db
@pytest.fixture()
def get_castle():
    def wrapper(name):
        return Castle.objects.get(name=name)

    return wrapper


@pytest.mark.django_db
@pytest.fixture()
def warrior_model():
    return Warrior


@pytest.mark.django_db
@pytest.fixture()
def army_model():
    return Army
