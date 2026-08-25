from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._url = "https://automationexercise.com/"

    def goto(self) -> "HomePage":
        # Переходим на страницу, ожидая готовности DOM
        self.page.goto(self._url, wait_until="domcontentloaded")
        return self
