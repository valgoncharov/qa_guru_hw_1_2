import pytest
import requests
from http import HTTPStatus
from models.User import User


class TestSmoke:
    @pytest.mark.smoke('Smoke')
    def test_app_status(self, app_url: str):
        response = requests.get(f"{app_url}/api/status")
        assert response.status_code == HTTPStatus.OK

    def test_smoke_users(self, app_url: str):
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
