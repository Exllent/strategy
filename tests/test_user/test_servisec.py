import pytest
from user.services import auto_slug


@pytest.mark.parametrize("text, result", [
    ("Михаил", "mihail"),
    ("Кракен", "kraken"),
    ("убийца228", "ubijtsa228"),
    ("", "_anonim"),
    ([1, 2], '_anonim')
])



def test_auto_slug(text, result):
    result_auto_slug = auto_slug(text)
    assert result_auto_slug == result or result in result_auto_slug


# def test_client(client):
#     response = client.get()