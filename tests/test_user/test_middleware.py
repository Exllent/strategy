import pytest
from django.urls import reverse_lazy


@pytest.mark.parametrize("user, status_code", [
    ("not_authenticated", 403),
    ("authenticated", 403),
    ("admin_authenticated", 200)
])
def test_forbidden_admin_page_middleware(create_user, create_castle, client, create_admin, user, status_code):
    url = "/admin/"
    match user:
        case "not_authenticated":
            response = client.get(url)
            assert response.status_code == status_code
        case "authenticated":
            client.force_login(create_user)
            auth_response = client.get(url)
            assert auth_response.status_code == status_code
        case "admin_authenticated":
            client.force_login(create_admin)
            auth_admin_response = client.get(url)
            assert auth_admin_response.status_code == status_code


@pytest.mark.parametrize("url, status_code", [
    ("register", 200),
    ("register2", 302),
    ("authorization_code", 302),
    ("home", 302),
    ("login", 200)
])
def test_check_authenticate_user_middleware(client, url, status_code):
    response = client.get(reverse_lazy(url))
    assert response.status_code == status_code
