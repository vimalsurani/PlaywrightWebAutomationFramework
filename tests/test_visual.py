from pathlib import Path
from pytest_regressions.data_regression import DataRegressionFixture
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestVisual:
    BASE_SCREENSHOT_PATH = Path("screenshots")  # Base path for screenshots

    def test_visual_inventory_page(self, setup, data_regression: DataRegressionFixture):
        page = setup
        login_page = LoginPage(page)

        self._login_to_application(login_page)

        screenshot_path = self._capture_screenshot(page, "inventory_page.png")

        self._perform_regression_check(data_regression, screenshot_path)

    def test_visual_cart_page(self, setup, data_regression: DataRegressionFixture):
        page = setup
        login_page = LoginPage(page)

        self._login_to_application(login_page)

        page.click('.shopping_cart_link')
        screenshot_path = self._capture_screenshot(page, "cart_page.png")

        self._perform_regression_check(data_regression, screenshot_path)

    def test_visual_checkout_page(self, setup, data_regression: DataRegressionFixture):
        page = setup
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        self._login_to_application(login_page)

        inventory_page.add_items_to_cart(3)

        inventory_page.go_to_cart()
        page.click('.checkout_button')

        screenshot_path = self._capture_screenshot(page, "checkout_page.png")

        self._perform_regression_check(data_regression, screenshot_path)

    def _login_to_application(self, login_page: LoginPage):
        login_page.login('standard_user', 'secret_sauce')

    def _capture_screenshot(self, page, filename: str):
        screenshot_path = self.BASE_SCREENSHOT_PATH / filename
        page.screenshot(path=str(screenshot_path))
        return str(screenshot_path)

    def _perform_regression_check(self, data_regression: DataRegressionFixture, screenshot_path: str):
        data_regression.check(screenshot_path)

