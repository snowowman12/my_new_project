"""
Те же тесты, но через pytest-mock: mocker.patch('requests.get').

Отличие от подхода с `responses`:
  - здесь подменяется сама функция requests.get (становится MagicMock),
    а fake-Response мы собираем руками (FakeResponse ниже). Ничего про
    HTTP-протокол, adapter или "какой запрос был бы отправлен" не
    проверяется — мокаем на уровне Python-объекта, а не сетевого протокола.
  - патчить нужно именно ту ссылку, которую использует код под тестом
    (app.client.requests.get, т.е. имя так, как оно импортировано внутри
    app/client.py) — патч не по тому пути молча ничего не мокает,
    классическая ошибка этого подхода.
  - мы сами отвечаем за то, чтобы fake-объект вёл себя как настоящий
    requests.Response (status_code, .json(), .raise_for_status()) — если
    забыть корректно реализовать raise_for_status(), сломанный клиент
    может пройти тест, который должен был упасть.
  - плюс: проще и быстрее для одного вызова, не требует отдельной
    HTTP-мокинг библиотеки, если pytest-mock уже используется в проекте
    для других целей.

Изоляция от интернета: реальный requests.get вообще не вызывается — на
время теста имя подменено моком, поэтому перехватывать сетевой запрос
не приходится — его физически нет.
"""

import pydantic
import pytest
import requests

from client import get_post


class FakeResponse:
    """Минимальная замена requests.Response, собранная вручную."""

    def __init__(self, json_data, status_code):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if 400 <= self.status_code:
            raise requests.HTTPError(response=self)


def test_get_post_success(mocker):
    fake_response = FakeResponse(
        {"userId": 1, "id": 1, "title": "sample title", "body": "sample body"},
        status_code=200,
    )
    mock_get = mocker.patch("client.requests.get", return_value=fake_response)

    post = get_post(1)

    assert post.id == 1
    assert post.userId == 1
    assert post.title == "sample title"
    assert post.body == "sample body"
    mock_get.assert_called_once()
    assert "/posts/1" in mock_get.call_args.args[0]


def test_get_post_invalid_payload_fails_validation(mocker):
    fake_response = FakeResponse(
        {"userId": "not-an-int", "id": 1, "title": "t"},  # нет `body`
        status_code=200,
    )
    mocker.patch("client.requests.get", return_value=fake_response)

    with pytest.raises(pydantic.ValidationError):
        get_post(1)


def test_get_post_404(mocker):
    fake_response = FakeResponse({"error": "not found"}, status_code=404)
    mocker.patch("client.requests.get", return_value=fake_response)

    with pytest.raises(requests.HTTPError) as exc_info:
        get_post(1)

    assert exc_info.value.response.status_code == 404


def test_get_post_500(mocker):
    fake_response = FakeResponse({"error": "server error"}, status_code=500)
    mocker.patch("client.requests.get", return_value=fake_response)

    with pytest.raises(requests.HTTPError) as exc_info:
        get_post(1)

    assert exc_info.value.response.status_code == 500