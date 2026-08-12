# test_module_two.py

import pytest
from datetime import datetime


def get_now():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def test_api_auth(api_client):
    print(
        f"[{get_now()}][TEST] Проверка авторизации во втором файле через {api_client['base_url']}..."
    )
    assert "example.com" in api_client["base_url"]
