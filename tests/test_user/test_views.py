import pytest
from django.urls import reverse_lazy
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    "route_name, form_name",
    [
        ("register", "UserFirstRegisterForm"),
        ("register2", "UserSecondRegisterForm"),
        ("login", "UserLoginForm"),
        ("logout", ...),
        ("authorization_code", "AuthorizationEmailForm"),
    ],
)
@pytest.mark.django_db
def test_views(client, route_name, form_name, create_admin):
    client.force_login(user=create_admin)
    response = client.get(reverse_lazy(route_name))
    if route_name != "logout":
        assert form_name in str(response.context)


@pytest.mark.parametrize(
    "route_name, status_code, target_url",
    [
        ("register", 302, "home"),
        ("register2", 302, "home"),
        ("login", 302, "home"),
        ("logout", 302, "register"),
        ("authorization_code", 302, "home"),
    ],
)
@pytest.mark.django_db
def test_user_redirect(
    client, create_user, create_castle, route_name, status_code, target_url
):
    client.force_login(create_user)
    response = client.get(reverse_lazy(route_name))
    assertRedirects(
        response,
        expected_url=reverse_lazy(target_url),
        status_code=status_code,
        target_status_code=200,
    )


@pytest.mark.parametrize(
    "route_name, status_code",
    [
        ("register", 200),
        ("register2", 200),
        ("login", 200),
        ("authorization_code", 200),
        ("logout", 302),
    ],
)
@pytest.mark.django_db
def test_admin_redirect(client, create_admin, route_name, status_code):
    client.force_login(create_admin)
    response = client.get(reverse_lazy(route_name))
    assert response.status_code == status_code


@pytest.mark.django_db
def test_user_login(client, create_castle, create_user):
    response = client.post(
        reverse_lazy("login"),
        data={"username": "login_user", "password": "password_user"},
    )

    assertRedirects(
        response=response, expected_url="/", status_code=302, target_status_code=200
    )


def test_user_logout(client):
    response = client.get(reverse_lazy("logout"))
    assertRedirects(
        response,
        expected_url=reverse_lazy("register"),
        status_code=302,
        target_status_code=200,
    )


@pytest.mark.django_db
def test_register(client):
    response = client.post(
        reverse_lazy("register"),
        data={
            "login": "login",
            "email": "email@gmail.com",
            "password1": "asdfgh12345",
            "password2": "asdfgh12345",
        },
    )
    assertRedirects(
        response,
        expected_url=reverse_lazy("authorization_code"),
        status_code=302,
        target_status_code=200,
    )
    return client.session.get("code").values()


@pytest.mark.django_db
def test_authorization_email(client):
    (code,) = test_register(client)
    response = client.post(reverse_lazy("authorization_code"), data={"code": code})
    assertRedirects(
        response,
        expected_url=reverse_lazy("register2"),
        status_code=302,
        target_status_code=200,
    )
    return client


@pytest.mark.django_db
def test_second_register(client, create_race):
    return_client = test_authorization_email(client)
    data = {"nickname": "nickname123", "castle_name": "Los_angeles", "race": "Гномы_3"}
    response = return_client.post(reverse_lazy("register2"), data=data)
    assertRedirects(
        response,
        expected_url=reverse_lazy("home"),
        status_code=302,
        target_status_code=200,
    )


@pytest.mark.parametrize(
    "attribute, result",
    [
        ("login", "login"),
        ("nickname", "nickname123"),
        ("email", "email@gmail.com"),
        ("is_active", True),
        ("is_staff", False),
        ("is_superuser", False),
        ("is_registered", True),
        ("slug", "nickname123"),
        ("race", "Гномы"),
        ("castle", "Los_angeles"),
        ("silver_money", 0),
        ("gold_money", 0),
    ],
)
@pytest.mark.django_db
def test_full_register(
    client, create_race, django_user_model, attribute, result, get_race, get_castle
):
    test_second_register(client, create_race)
    user = django_user_model.objects.get(pk=1)
    match attribute:
        case "race":
            assert getattr(user, attribute) == get_race(result)
        case "castle":
            assert getattr(user, attribute) == get_castle(result)
        case _:
            assert getattr(user, attribute) == result
