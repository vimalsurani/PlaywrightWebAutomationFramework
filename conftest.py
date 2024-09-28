import pytest
from playwright.sync_api import Playwright, sync_playwright


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p


def launch_browser(playwright, headless: bool):
    return playwright.chromium.launch(args=['--start-maximized'], headless=headless)


def create_context(browser):
    return browser.new_context(
        no_viewport=True,
    )


def open_page(context):
    page = context.new_page()
    page.goto("https://www.saucedemo.com/")
    page.evaluate("window.moveTo(0, 0); window.resizeTo(window.screen.availWidth, window.screen.availHeight);")
    return page


@pytest.fixture()
def setup(playwright, request):
    # Get headless option from command line argument
    headless = request.config.getoption("--headless")
    browser = launch_browser(playwright, headless)
    context = create_context(browser)
    page = open_page(context)

    yield page

    page.close()
    context.close()
    browser.close()


@pytest.fixture()
def login(setup):
    page = setup
    page.fill('[data-test="username"]', 'standard_user')
    page.fill('[data-test="password"]', 'secret_sauce')
    page.click('[data-test="login-button"]')

    # Verify login was successful
    assert page.is_visible('.inventory_list'), "Login failed: Inventory page not visible."


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode.")
