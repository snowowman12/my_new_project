from playwright.sync_api import Page
from pages.base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._view_product_links = page.get_by_role("link", name=" View Product")

    def click_first_view_product(self):
        from pages.product_detail_page import ProductDetailPage

        self._view_product_links.first.click()
        return ProductDetailPage(self.page)
