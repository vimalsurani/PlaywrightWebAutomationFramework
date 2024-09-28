import allure
import json
import pytest
from playwright.sync_api import Page
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


class TestAccessibility:

    @allure.feature('Accessibility Testing')
    @allure.story('Inventory Page Accessibility Check')
    @pytest.mark.accessibility
    @pytest.mark.smoke
    def test_accessibility_inventory_page(self, login, setup: Page):
        page = setup
        self._check_accessibility(page, page.url)

    @allure.feature('Accessibility Testing')
    @allure.story('Cart Page Accessibility Check')
    @pytest.mark.accessibility
    @pytest.mark.regression
    def test_accessibility_cart_page(self, login, setup: Page):
        page = setup
        inventory_page = InventoryPage(page)
        inventory_page.go_to_cart()  # Navigate to Cart page
        self._check_accessibility(page, page.url)

    @allure.feature('Accessibility Testing')
    @allure.story('Checkout Page Accessibility Check')
    @pytest.mark.accessibility
    @pytest.mark.regression
    def test_accessibility_checkout_page(self, login, setup: Page):
        page = setup
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)

        inventory_page.go_to_cart()  # Navigate to Cart page
        cart_page.proceed_to_checkout()  # Proceed to Checkout
        self._check_accessibility(page, page.url)

    def _check_accessibility(self, page: Page, url: str):
        with allure.step(f"Navigate to the page: {url}"):
            page.goto(url)

        with allure.step("Inject axe-core for accessibility testing"):
            self._inject_axe(page)

        with allure.step("Run accessibility checks using axe-core"):
            page.evaluate("axe.run().then(results => window.axeResults = results);")
            results = page.evaluate("() => window.axeResults")

        with allure.step("Check and report accessibility violations"):
            if results['violations']:
                allure.attach(
                    json.dumps(results['violations'], indent=4),
                    name="Accessibility Violations",
                    attachment_type=allure.attachment_type.JSON
                )
                for violation in results['violations']:
                    print(f"Violation: {violation['description']} (Impact: {violation['impact']})")
                    print(f"  Tags: {violation['tags']}")
                    print(f"  Nodes: {violation['nodes']}")

        assert len(results['violations']) == 0, f"Accessibility violations found: {results['violations']}"

    @staticmethod
    def _inject_axe(page: Page):
        page.evaluate("""() => {
            return new Promise((resolve) => {
                const script = document.createElement('script');
                script.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.1.1/axe.min.js';
                script.onload = resolve;
                document.head.appendChild(script);
            });
        }""")
