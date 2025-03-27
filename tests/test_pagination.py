import pytest
from http import HTTPStatus
import requests
from random import randint
from typing import Dict, Any


def test_default_page_size(app_url: str) -> None:
    """
    Проверить, что размер страницы по возвращает ожидаемое
    количество элементов и соответствует общему количеству.

    """
    response = requests.get(f"{app_url}/users")
    assert response.status_code == HTTPStatus.OK

    result: Dict[str, Any] = response.json()
    total: int = result["total"]
    items_count: int = len(result["items"])

    assert total == items_count, "Общее количество должно соответствовать количеству элементов"


@pytest.mark.parametrize('size', [1, 3, 5])
def test_custom_page_size(app_url: str, size: int) -> None:
    """
    Проверить пагинацию с разными размерами страниц.

        app_url: Главный URL приложения
        size: Количество элементов на странице

    """
    response = requests.get(
        f"{app_url}/users", params={'page': 1, 'size': size})
    assert response.status_code == HTTPStatus.OK

    result: Dict[str, Any] = response.json()
    items: list = result['items']

    assert len(items) == size, f"На странице присутствует {size} элементов"
    assert result['size'] == size, "Размер страницы соответствует запрошенному размеру"
    assert result['page'] == 1, "Должен быть на первой странице"
    assert result['total'] > 0, "Общее количество элементов должно быть больше 0"


def test_random_page_size(app_url: str) -> None:
    """
    Проверить пагинацию с различным указанием страниц
    """
    size: int = randint(1, 13)
    response = requests.get(f"{app_url}/users", params={"size": size})
    assert response.status_code == HTTPStatus.OK

    result: Dict[str, Any] = response.json()
    assert len(result["items"]
               ) == size, f"На странице присутствует {size} элементов"


@pytest.mark.parametrize('page', [1, 2, 3])
def test_page_navigation(app_url: str, page: int) -> None:
    """
    Проверить навигацию по разным страницам.

        app_url: Главный URL приложения
        page: Номер страницы
    """
    response = requests.get(
        f"{app_url}/users", params={"page": page, "size": 5})
    assert response.status_code == HTTPStatus.OK

    result: Dict[str, Any] = response.json()
    assert result['page'] == page, f"Должна быть страница {page}"
    assert len(result['items']) > 0, "На странице должны быть элементы"
