from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._cart_info_table = page.locator("#cart_info")

    def verify_cart_is_visible(self) -> "CartPage":
        # Веб-ферст ассершн вместо wait_for_timeout()
        expect(self._cart_info_table).to_be_visible()
        return self
