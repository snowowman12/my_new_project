"""
Тесты для client.get_post с использованием библиотеки `responses`.

`responses` подменяет транспортный adapter, который `requests` использует
внутри себя. Из этого следует:
  - мокается ЛЮБОЙ вызов requests.get/post/... в коде под тестом, независимо
    от того, откуда именно был импортирован `requests`;
  - библиотека сама проверяет, что URL/метод/параметры реально совпали
    с зарегистрированным моком, и может падать на несовпадениях;
  - это специализированный инструмент именно под HTTP-мокинг requests, поэтому
    код читается как "вот фейковый сетевой ответ", а не как generic-мок.

Реальных сетевых запросов в этих тестах нет: `responses` сам бросает
ConnectionError при попытке обратиться к незарегистрированному URL —
изоляция от интернета гарантируется самой библиотекой.
"""

import pydantic
import pytest
import requests
import responses

from client import BASE_URL, get_post


@responses.activate
def test_get_post_success():
    responses.add(
        responses.GET,
        f"{BASE_URL}/posts/1",
        json={
            "userId": 1,
            "id": 1,
            "title": "sample title",
            "body": "sample body",
        },
        status=200,
    )

    post = get_post(1)

    assert post.id == 1
    assert post.userId == 1
    assert post.title == "sample title"
    assert post.body == "sample body"
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == f"{BASE_URL}/posts/1"


@responses.activate
def test_get_post_invalid_payload_fails_validation():
    """Если форма ответа API сломалась, это должен ловить pydantic, а не requests."""
    responses.add(
        responses.GET,
        f"{BASE_URL}/posts/1",
        json={"userId": "not-an-int", "id": 1, "title": "t"},  # нет `body`
        status=200,
    )

    with pytest.raises(pydantic.ValidationError):
        get_post(1)


@responses.activate
def test_get_post_404():
    responses.add(
        responses.GET,
        f"{BASE_URL}/posts/1",
        json={"error": "not found"},
        status=404,
    )

    with pytest.raises(requests.HTTPError) as exc_info:
        get_post(1)

    assert exc_info.value.response.status_code == 404


@responses.activate
def test_get_post_500():
    responses.add(
        responses.GET,
        f"{BASE_URL}/posts/1",
        json={"error": "server error"},
        status=500,
    )

    with pytest.raises(requests.HTTPError) as exc_info:
        get_post(1)

    assert exc_info.value.response.status_code == 500