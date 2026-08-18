import pytest
from playwright.sync_api import expect


@pytest.mark.ui
def test_example(page):
    page.goto("https://www.saucedemo.com/")
    expect(page).to_have_title("Swag Labs")
