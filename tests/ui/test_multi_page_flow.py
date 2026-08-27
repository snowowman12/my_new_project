from playwright.sync_api import Page
from pages.home_page import HomePage


def test_add_to_cart_from_details_flow(page: Page):
    home_page = HomePage(page)

    # Выстраиваем шаги с автоматическим переключением контекста страниц
    product_detail_page = (
        home_page.goto().click_home().click_products().click_first_view_product()
    )

    # Добавляем в корзину и переходим в нее через базовый элемент и проверяем
    cart_page = product_detail_page.click_add_to_cart().click_cart()

    cart_page.verify_cart_is_visible()
