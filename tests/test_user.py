from http import HTTPStatus

import pytest
import requests
from models.users_model import UserData
from random import randint
from fastapi_pagination import Page


class TestUserData:

    def test_users(self, app_url):
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
        users_data = response.json()
        Page[UserData].model_validate(users_data)

    def test_user(self, app_url):
        user_id = randint(1, 13)
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK

        user = response.json()
        UserData.model_validate(user)

    @pytest.mark.parametrize("user_id", [111])
    def test_nonexistent_user(self, app_url, user_id):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", ["str", 0, -1, 1.1, " "])
    def test_user_data_type(self, app_url, user_id):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
