import pytest
from http import HTTPStatus

import requests
from random import randint


def test_count_items(app_url):
    """
    Проверка количества отображения данных
    :param app_url:
    :return:
    """
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    result = response.json()

    total = result["total"]
    expected_page_count = len(result["items"])
    assert total == expected_page_count


@pytest.mark.parametrize('size', (1, 3, 5))
def test_count_users_on_page_by_param_change(app_url, size):
    """
    Проверка количества пользователей на странице, при разном параметре size
    :param page:
    :param size:
    """
    response = requests.get(f'{app_url}', params={'page': 1, 'size': size})
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    items = body['items']
    assert len(items) == size
    assert body['size'] == size
    assert body['page'] == 1
    assert body['total']


def test_pagination_count_object_first_pages(app_url):
    """
    Проверка на количество объектов на первой странице
    :param app_url:
    :return:
    """

    size = randint(1, 13)
    response = requests.get(f"{app_url}/api/users/", params={"size": size})
    assert response.status_code == HTTPStatus.OK

    result = response.json()
    object_count_actual = len(result["items"])
    assert object_count_actual == size