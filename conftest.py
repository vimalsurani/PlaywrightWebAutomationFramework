import pytest
import allure
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright
from pytest_regressions.data_regression import DataRegressionFixture

# Create directories for the data regression files and screenshots if they don't exist
data_dir = Path("data_regression")
data_dir.mkdir(parents=True, exist_ok=True)
screenshots_dir = Path("screenshots")
screenshots_dir.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p


def launch_browser(playwright, headless: bool):
    return playwright.chromium.launch(args=['--start-maximized'], headless=headless)


def create_context(browser):
    return browser.new_context(
        no_viewport=True,
        record_video_dir="videos/",
        record_video_size={"width": 1280, "height": 720},
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

    # Attach video recording to Allure report
    video_path = page.video.path()
    allure.attach.file(video_path, name="Test Video", attachment_type=allure.attachment_type.WEBM)

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


@pytest.fixture()
def data_regression(request) -> DataRegressionFixture:
    return DataRegressionFixture(
        request=request,  # Pass request explicitly
        datadir=data_dir,
        original_datadir=data_dir
    )


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode.")
