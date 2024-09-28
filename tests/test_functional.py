from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestFunctional:

    def test_verify_za_sorting(self, setup):
        page = setup
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        self._login(login_page)

        inventory_page.sort_items_by('za')

        item_names = inventory_page.get_item_names()
        sorted_names = sorted(item_names, reverse=True)
        assert item_names == sorted_names, f"Items are not sorted in Z-A order: {item_names} != {sorted_names}"

    def test_verify_high_low_price_sorting(self, setup):
        page = setup
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        self._login(login_page)

        inventory_page.sort_items_by('hilo')

        item_prices = inventory_page.get_item_prices()
        sorted_prices = sorted(item_prices, reverse=True)
        assert item_prices == sorted_prices, f"Prices are not sorted from high to low: {item_prices} != {sorted_prices}"

    def test_add_multiple_items_and_checkout(self, setup):
        page = setup
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)

        self._login(login_page)

        inventory_page.add_items_to_cart(3)

        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(page)
        checkout_page.fill_checkout_form('David', 'Cameron', '96375')
        checkout_page.finish_checkout()

        order_message = page.locator('.complete-header').inner_text()
        assert order_message == 'Thank you for your order!', f"Order completion message is incorrect: {order_message}"

    def _login(self, login_page):
        login_page.login('standard_user', 'secret_sauce')
