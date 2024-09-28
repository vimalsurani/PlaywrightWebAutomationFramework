from pathlib import Path
import allure
import pytest
from pytest_regressions.data_regression import DataRegressionFixture
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage


class TestVisual:
    BASE_SCREENSHOT_PATH = Path("screenshots")  # Base path for screenshots

    @allure.feature('Visual Testing')
    @allure.story('Inventory Page Visual Comparison')
    @pytest.mark.visual
    def test_visual_inventory_page(self, setup, data_regression: DataRegressionFixture):
        page = setup
        login_page = LoginPage(page)

        self._login_to_application(login_page)

        with allure.step("Capture screenshot of Inventory page"):
            screenshot_path = self._capture_screenshot(page, "inventory_page.png")

        with allure.step("Perform data regression check on Inventory page screenshot"):
            self._perform_regression_check(data_regression, screenshot_path)

    @allure.feature('Visual Testing')
    @allure.story('Cart Page Visual Comparison')
    @pytest.mark.visual
    def test_visual_cart_page(self, setup, data_regression: DataRegressionFixture):
        page = setup
        login_page = LoginPage(page)

        self._login_to_application(login_page)

        with allure.step("Navigate to cart page and capture screenshot"):
            page.click('.shopping_cart_link')
            screenshot_path = self._capture_screenshot(page, "cart_page.png")

        with allure.step("Perform data regression check on Cart page screenshot"):
            self._perform_regression_check(data_regression, screenshot_path)

    @allure.feature('Visual Testing')
    @allure.story('Checkout Page Visual Comparison')
    @pytest.mark.visual
    @pytest.mark.regression
    def test_visual_checkout_page(self, setup, data_regression: DataRegressionFixture):
        page = setup
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        self._login_to_application(login_page)

        with allure.step("Add an item to the cart"):
            inventory_page.add_items_to_cart(3)

        with allure.step("Proceed to checkout"):
            inventory_page.go_to_cart()
            page.click('.checkout_button')

        with allure.step("Capture screenshot of Checkout page"):
            screenshot_path = self._capture_screenshot(page, "checkout_page.png")

        with allure.step("Perform data regression check on Checkout page screenshot"):
            self._perform_regression_check(data_regression, screenshot_path)

    def _login_to_application(self, login_page: LoginPage):
        with allure.step("Login to the application"):
            login_page.login('standard_user', 'secret_sauce')

    def _capture_screenshot(self, page, filename: str):
        screenshot_path = self.BASE_SCREENSHOT_PATH / filename
        page.screenshot(path=str(screenshot_path))
        allure.attach.file(str(screenshot_path), name=filename.split('.')[0], attachment_type=allure.attachment_type.PNG)
        return str(screenshot_path)

    def _perform_regression_check(self, data_regression: DataRegressionFixture, screenshot_path: str):
        try:
            data_regression.check(screenshot_path)
        except Exception as e:
            allure.attach(f"Regression check failed: {str(e)}", name="Error", attachment_type=allure.attachment_type.TEXT)
            raise