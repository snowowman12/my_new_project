import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize("query", ["qa", "aqa", "python"])
@pytest.mark.ui
def test_search_param(page: Page, query: str) -> None:
    page.goto("https://www.bing.com/")

    # через role (наиболее приближен к Playwright best practices)
    search_input = page.get_by_role("combobox")
    search_input.fill(query)
    search_input.press("Enter")

    results = page.locator("li.b_algo")
    expect(results.first).to_be_visible(timeout=10000)

    # результатов поиска не жёстко 5 штук, по заданию "минимум 5"
    assert results.count() >= 5
