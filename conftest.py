# conftest.py
import pytest
import time
from datetime import datetime


# Вспомогательная функция для красивого вывода таймстемпов
def get_now():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


# 1. Фикстура с scope="session"
@pytest.fixture(scope="session")
def api_client():
    print(f"\n[{get_now()}][SESSION] Инициализация глобального API-клиента...")
    client = {"base_url": "https://api.example.com", "token": "secret_abc123"}
    yield client
    print(f"\n[{get_now()}][SESSION] Закрытие глобального API-клиента.")

    # 2. Фикстура с autouse=True и фазой yield/teardown
    @pytest.fixture(autouse=True)
    def benchmark_logger():
        # Phase: Setup
        start_time = time.time()
        print(f"\n[{get_now()}][AUTOUSE] >>> Старт теста.")

        yield

        # Phase: Teardown
        end_time = time.time()
        duration = end_time - start_time
        print(
            f"\n[{get_now()}][AUTOUSE] <<< Тест завершен. Длительность: {duration:.4f} сек."
        )
