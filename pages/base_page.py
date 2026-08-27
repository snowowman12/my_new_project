from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self._home_link = page.get_by_role("link", name=" Home")
        self._products_link = page.get_by_role("link", name=" Products")
        self._cart_link = page.get_by_role("link", name="View Cart")

    def click_home(self):
        from pages.home_page import HomePage

        self._home_link.click()
        return HomePage(self.page)

    def click_products(self):
        from pages.products_page import ProductsPage

        self._products_link.click()
        return ProductsPage(self.page)

    def click_cart(self):
        from pages.cart_page import CartPage

        self._cart_link.click()
        return CartPage(self.page)
