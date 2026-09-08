# Базовый GET с Session и таймаутом

import requests
from requests import Session

BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10  # именованная константа вместо магического числа


def get_post(session: Session, post_id: int) -> dict:
    """Получить пост по ID. Возвращает JSON или вызывает исключение."""
    url = f"{BASE_URL}/posts/{post_id}"
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()  # выбросит HTTPError при 4xx/5xx
    return response.json()


# Использование
with requests.Session() as session:
    post = get_post(session, 1)
    print(post["title"])


# POST + обработка ошибок


def create_post(session: Session, title: str, body: str, user_id: int) -> dict:
    url = f"{BASE_URL}/posts"
    payload = {"title": title, "body": body, "userId": user_id}
    try:
        response = session.post(url, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("Сервер не ответил за 10 секунд") from None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            raise ValueError("Некорректные данные поста") from e
        raise


# dataclass (простой случай)

from dataclasses import dataclass


@dataclass
class PostSimple:
    userId: int
    id: int
    title: str
    body: str


from pydantic import BaseModel, Field, field_validator, ConfigDict

# Выносим константы на уровень модуля или конфигурации
MIN_TITLE_LENGTH = 1
MAX_TITLE_LENGTH = 200
MIN_BODY_LENGTH = 1
MIN_ID_VALUE = 1  # Заменяет gt=0 на ge=MIN_ID_VALUE (greater or equal)


class Post(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    userId: int = Field(..., ge=MIN_ID_VALUE, description="ID автора поста")
    id: int = Field(..., ge=MIN_ID_VALUE, description="ID поста")
    title: str = Field(..., min_length=MIN_TITLE_LENGTH, max_length=MAX_TITLE_LENGTH)
    body: str = Field(..., min_length=MIN_BODY_LENGTH)

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        # strip() лучше делать до проверки длины pydantic,
        # но в рамках валидатора оставляем логику чистки
        v_stripped = v.strip()
        if not v_stripped:
            raise ValueError("Заголовок не может быть пустым или состоять из пробелов")
        return v_stripped
