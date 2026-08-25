from playwright.sync_api import Page
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._add_to_cart_button = page.get_by_role("button", name=" Add to cart")

    def click_add_to_cart(self) -> "ProductDetailPage":
        self._add_to_cart_button.click()
        return self
