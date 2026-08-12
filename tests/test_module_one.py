# test_module_one.py
import pytest
import time
from datetime import datetime


def get_now():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


# 3. Фикстура с scope="module" и фазой teardown (yield)
@pytest.fixture(scope="module")
def db_connection():
    print(f"\n[{get_now()}][MODULE-1] --- Подключение к БД (Один раз на модуль) ---")
    connection = "Active_DB_Connection"

    yield connection

    print(f"\n[{get_now()}][MODULE-1] --- Отключение от БД (Teardown модуля) ---")


def test_database_query_heavy(db_connection, api_client):
    print(f"[{get_now()}][TEST] Выполнение тяжелого запроса через {db_connection}...")
    time.sleep(0.1)  # Имитация работы
    assert api_client["token"] == "secret_abc123"


def test_database_query_light(db_connection):
    print(f"[{get_now()}][TEST] Выполнение легкого запроса через {db_connection}...")
    time.sleep(0.05)
    assert db_connection == "Active_DB_Connection"
