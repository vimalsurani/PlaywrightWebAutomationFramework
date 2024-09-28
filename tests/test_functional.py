import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestFunctional:

    @allure.feature('Sorting Verification')
    @allure.story('Verify Z-A Sorting on Inventory Page')
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_verify_za_sorting(self, setup):
        page = setup
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        self._login(login_page)

        with allure.step("Sort items in Z-A order"):
            inventory_page.sort_items_by('za')

        with allure.step("Validate Z-A sorting"):
            item_names = inventory_page.get_item_names()
            sorted_names = sorted(item_names, reverse=True)
            assert item_names == sorted_names, f"Items are not sorted in Z-A order: {item_names} != {sorted_names}"

    @allure.feature('Sorting Verification')
    @allure.story('Verify High to Low Price Sorting on Inventory Page')
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_verify_high_low_price_sorting(self, setup):
        page = setup
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        self._login(login_page)

        with allure.step("Sort items by price from High to Low"):
            inventory_page.sort_items_by('hilo')

        with allure.step("Validate High-Low sorting"):
            item_prices = inventory_page.get_item_prices()
            sorted_prices = sorted(item_prices, reverse=True)
            assert item_prices == sorted_prices, f"Prices are not sorted from high to low: {item_prices} != {sorted_prices}"

    @allure.feature('Cart Functionality')
    @allure.story('Add Multiple Items and Checkout')
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_add_multiple_items_and_checkout(self, setup):
        page = setup
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)

        self._login(login_page)

        with allure.step("Add multiple items to the cart"):
            inventory_page.add_items_to_cart(3)

        with allure.step("Proceed to checkout"):
            inventory_page.go_to_cart()
            cart_page.proceed_to_checkout()

        with allure.step("Complete checkout"):
            checkout_page = CheckoutPage(page)
            checkout_page.fill_checkout_form('David', 'Cameron', '96375')
            checkout_page.finish_checkout()

        with allure.step("Verify order completion"):
            order_message = page.locator('.complete-header').inner_text()
            assert order_message == 'Thank you for your order!', f"Order completion message is incorrect: {order_message}"

    def _login(self, login_page):
        with allure.step("Login to the application"):
            login_page.login('standard_user', 'secret_sauce')
