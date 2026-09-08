import pytest
import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from api_models import Post  # Импортируем модель из созданного ранее api_models.py

# =====================================================================
# КОНСТАНТЫ И НАСТРОЙКИ (Критерий: без магических чисел)
# =====================================================================
BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT_SECONDS = 5.0


# =====================================================================
# ВСПOMOГАТЕЛЬНЫЕ ФУНКЦИИ КЛИЕНТА
# =====================================================================


def get_post(session: requests.Session, post_id: int) -> dict:
    """Получает пост по его ID с использованием сессии.

    Возвращает dict с данными поста или выбрасывает исключение.
    """
    url = f"{BASE_URL}/posts/{post_id}"

    try:
        response = session.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()

    except HTTPError as http_err:
        raise RuntimeError(
            f"Не удалось получить пост {post_id}. Ошибка HTTP: {http_err}. "
            f"Проверьте правильность ID поста или доступность эндпоинта."
        ) from http_err
    except Timeout as timeout_err:
        raise RuntimeError(
            f"Превышено время ожидания ({TIMEOUT_SECONDS}с) при получении поста {post_id}. "
            f"Проверьте стабильность интернет-соединения или статус API."
        ) from timeout_err


def create_post(session: requests.Session, title: str, body: str, user_id: int) -> dict:
    """Создает новый пост с обработкой Timeout и HTTPError.

    Возвращает dict с данными созданного поста.
    """
    url = f"{BASE_URL}/posts"
    payload = {"title": title, "body": body, "userId": user_id}

    try:
        response = session.post(url, json=payload, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()

    except Timeout as timeout_err:
        raise RuntimeError(
            f"Не удалось отправить запрос на создание поста из-за таймаута ({TIMEOUT_SECONDS}с). "
            f"Пожалуйста, повторите попытку позже или увеличьте константу TIMEOUT_SECONDS."
        ) from timeout_err

    except HTTPError as http_err:
        status_code = http_err.response.status_code
        if status_code == 400:
            action = "Проверьте формат отправляемых данных (title, body, userId)."
        elif status_code == 403 or status_code == 401:
            action = "Проверьте права доступа или авторизационные токены."
        else:
            action = "Обратитесь к администратору сервера или проверьте статус-код."

        raise RuntimeError(
            f"Сервер вернул ошибку {status_code} при создании поста. Действие: {action}"
        ) from http_err

    except RequestException as general_err:
        raise RuntimeError(
            f"Непредвиденная ошибка сети при создании поста: {general_err}. "
            f"Проверьте сетевое подключение."
        ) from general_err


# =====================================================================
# PYTEST ФИКСТУРЫ
# =====================================================================


@pytest.fixture(scope="session")
def api_session():
    """Фикстура для переиспользования HTTP-сессии (Критерий: requests.Session)."""
    with requests.Session() as session:
        yield session


# =====================================================================
# ТЕСТЫ API (С обновлёнными именами)
# =====================================================================


def test_get_post_validates_with_pydantic(api_session):
    """GET /posts/1 → получение через функцию + валидация через Post."""
    post_data = get_post(api_session, post_id=1)

    # Валидируем Pydantic-моделью. При ошибке тест упадет с понятным логом Pydantic
    post = Post.model_validate(post_data)
    assert post.id == 1


def test_get_posts_by_user_id(api_session):
    """GET /posts?userId=1 → список постов + валидация каждого."""
    url = f"{BASE_URL}/posts"
    params = {"userId": 1}

    response = api_session.get(url, params=params, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()

    posts_list = response.json()
    assert len(posts_list) > 0, "Список постов пуст"

    for raw_post in posts_list:
        post = Post.model_validate(raw_post)
        assert post.user_id == 1


def test_create_post_returns_201_and_validates(api_session):
    """POST /posts → создание через функцию + проверка статус-кода 201 и структуры."""
    title = "Тестовый заголовок"
    body = "Тестовый текст для проверки API"
    user_id = 1

    # jsonplaceholder при успешном POST возвращает статус 201 Created.
    # Чтобы проверить именно статус-код, сделаем прямой запрос или переиспользуем сессию
    url = f"{BASE_URL}/posts"
    payload = {"title": title, "body": body, "userId": user_id}

    response = api_session.post(url, json=payload, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()

    assert response.status_code == 201

    # Валидируем тело ответа через Pydantic
    created_post_data = response.json()
    post = Post.model_validate(created_post_data)

    assert post.title == title
    assert post.body == body
    assert post.user_id == user_id


def test_delete_post_returns_200_or_204(api_session):
    """DELETE /posts/1 → проверка статус-кода 200/204."""
    url = f"{BASE_URL}/posts/1"

    response = api_session.delete(url, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()

    # jsonplaceholder возвращает 200 OK при успешном DELETE
    assert response.status_code in [200, 204]
