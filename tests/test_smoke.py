import pytest
import requests
from http import HTTPStatus


@pytest.mark.smoke
def test_app_status(app_url: str):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == HTTPStatus.OK


def test_smoke_users(app_url: str):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK