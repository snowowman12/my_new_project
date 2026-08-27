# pages/login_page.py
from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        # Semantic-локаторы — лучший выбор для форм
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_container = page.locator(".error-message-container")

    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        expect(self.error_container).to_be_visible()
        return self.error_container.inner_text()
