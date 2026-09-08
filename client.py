import requests

from api_models import Post

BASE_URL = "https://jsonplaceholder.typicode.com"


def get_post(post_id: int) -> Post:
    """
    Получить пост по id и провалидировать ответ через pydantic-модель Post.

    Исключения:
        requests.HTTPError — если сервер вернул статус 4xx/5xx.
        pydantic.ValidationError — если тело ответа не соответствует схеме.
    """
    response = requests.get(f"{BASE_URL}/posts/{post_id}", timeout=5)
    response.raise_for_status()
    return Post(**response.json())