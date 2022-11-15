import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.parametrize(
    "url, template_name, status_code",
    [
        (
            "/register/",
            "register.html",
            200,
        ),
        ("/authorization_code/", "authorization.html", 200),
        ("/login/", "login.html", 200),
        ("/logout/", ..., 302),
        ("/register2/", "register2.html", 200),
    ],
)
@pytest.mark.django_db()
def test_templates_and_status_code(
    client, url, template_name, status_code, create_admin
):
    client.force_login(create_admin)
    response = client.get(url)
    assert response.status_code == status_code
    if url != "/logout/":
        assertTemplateUsed(response, template_name=f"user/{template_name}")
