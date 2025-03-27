from http import HTTPStatus

import pytest
import requests
from models.User import User
from random import randint
from fastapi_pagination import Page


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


class TestUserData:

    def test_users1(self, app_url):
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK

        users = response.json()
        for user in users:
            User.model_validate(user)

    @pytest.mark.parametrize("user_id", [1, 6, 14])
    def test_user1(self, app_url, user_id: int):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK

        user = response.json()
        User.model_validate(user)

    def test_users_no_duplicates(self, users):
        users_id = [user["id"] for user in users]
        assert len(users_id) == len(set(users_id))

    @pytest.mark.parametrize("user_id", [15])
    def test_user_invalid_values(self, app_url, user_id: int):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_users(self, app_url):
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
        users_data = response.json()
        Page[User].model_validate(users_data)

    def test_user(self, app_url):
        user_id = randint(1, 13)
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK

        user = response.json()
        User.model_validate(user)

    @pytest.mark.parametrize("user_id", [111])
    def test_nonexistent_user(self, app_url, user_id):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize("user_id", ["str", 0, -1, 1.1, " "])
    def test_user_data_type(self, app_url, user_id):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
