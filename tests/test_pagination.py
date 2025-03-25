from http import HTTPStatus

import requests
from random import randint


def test_count_items(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    result = response.json()

    total = result["total"]
    expected_page_count = len(result["items"])
    assert total == expected_page_count


def test_pagination_count_pages(app_url):
    """Проверка на количество страниц с рандомным значением size"""
    size = randint(1, 20)
    response = requests.get(f"{app_url}/api/users/", params={"size": size})
    assert response.status_code == HTTPStatus.OK

    result = response.json()
    total = result["total"]
    if total % size == 0:
        expected_page_count = total//size
    else:
        expected_page_count = total//size + 1

    result = response.json()
    actual_page_count = result["pages"]
    assert expected_page_count == actual_page_count


def test_pagination_count_object_first_pages(app_url):
    """Проверка на количество объектов на первой странице"""
    size = randint(1, 13)
    response = requests.get(f"{app_url}/api/users/", params={"size": size})
    assert response.status_code == HTTPStatus.OK

    result = response.json()
    object_count_actual = len(result["items"])
    assert object_count_actual == size


def test_pagination_count_object_last_pages(app_url):
    """Проверка на количество объектов на последней странице"""
    size = randint(1, 13)
    response = requests.get(f"{app_url}/api/users/", params={"size": size})
    assert response.status_code == HTTPStatus.OK
    result = response.json()
    total = result["total"]

    if total % size == 0:
        last_page_number = total//size
    else:
        last_page_number = total//size + 1

    response_last_page = requests.get(f"{app_url}/api/users/", params={"size": size, "page": last_page_number})
    assert response_last_page.status_code == HTTPStatus.OK
    object_count_last_page_expected = total % ((last_page_number - 1) * size)
    result_last_page = response_last_page.json()
    object_count_actual = len(result_last_page["items"])
    assert object_count_actual == object_count_last_page_expected


def test_pagination_compare_objects_pages(app_url):
    """Сравнение объектов на разных страницах"""
    size = randint(7, 13)
    response1 = requests.get(f"{app_url}/api/users/", params={"size": size, "page": 1})
    assert response1.status_code == HTTPStatus.OK
    result1 = response1.json()

    response2 = requests.get(f"{app_url}/api/users/", params={"size": size, "page": 2})
    assert response2.status_code == HTTPStatus.OK
    result2 = response2.json()

    assert result1 != result2 #проверка, что содержимое страниц не дублируется

    ids1 = {user['id'] for user in result1['items']}
    ids2 = {user['id'] for user in result2['items']}
    assert not (ids1 & ids2) #проверка, что id пользователей со страницы 1 отсутствуют на странице 2

    ids1_list = [user['id'] for user in result1['items']]
    assert len(ids1_list) == len(ids1) #проверка, что на странице 1 нет дублирующихся id пользователей
    ids2_list = [user['id'] for user in result2['items']]
    assert len(ids2_list) == len(ids2) #проверка, что на странице 2 нет дублирующихся id пользователей
