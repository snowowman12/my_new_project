# tests/ui/test_auth.py
import os
import pytest
from dotenv import load_dotenv
from pages.login_page import LoginPage
from playwright.sync_api import expect

load_dotenv()


@pytest.mark.ui
@pytest.mark.parametrize(
    "username, password",
    [
        # Передаем основной аккаунт (из .env или дефолтный)
        (
            os.getenv("SAUCE_USER", "standard_user"),
            os.getenv("SAUCE_PASS", "secret_sauce"),
        ),
        # Дополнительные валидные пользователи для проверки успешного входа
        ("problem_user", "secret_sauce"),
        ("performance_glitch_user", "secret_sauce"),
        ("visual_user", "secret_sauce"),
    ],
    ids=["env_user", "problem_user", "performance_user", "visual_user"],
)
def test_successful_login(page, username, password):
    login_page = LoginPage(page)
    page.goto("https://www.saucedemo.com")

    # Теперь используем переменные username и password из параметров pytest
    login_page.login(username, password)
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    # 2. Дополнительный assert: проверяем, что на новой странице виден заголовок каталога
    # (Предполагается, что на странице inventory есть элемент с текстом "Products")
    expect(page.get_by_text("Products")).to_be_visible()


@pytest.mark.ui
def test_locked_out_user(page):
    login_page = LoginPage(page)
    page.goto("https://www.saucedemo.com")

    login_page.login("locked_out_user", "secret_sauce")
    error = login_page.get_error_message()
    assert "Epic sadface" in error
    # Переводим проверку на стабильный expect от Playwright.
    # Он проверяет, что на странице появилось сообщение об ошибке блокировки.
    expect(page.get_by_text("Epic sadface: Sorry, this user has been locked out.")).to_be_visible()