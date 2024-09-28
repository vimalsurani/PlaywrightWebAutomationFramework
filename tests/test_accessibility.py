from playwright.sync_api import Page
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


class TestAccessibility:

    def test_accessibility_inventory_page(self, login, setup: Page):
        page = setup
        self._check_accessibility(page, page.url)

    def test_accessibility_cart_page(self, login, setup: Page):
        page = setup
        inventory_page = InventoryPage(page)
        inventory_page.go_to_cart()  # Navigate to Cart page
        self._check_accessibility(page, page.url)

    def test_accessibility_checkout_page(self, login, setup: Page):
        page = setup
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)

        inventory_page.go_to_cart()  # Navigate to Cart page
        cart_page.proceed_to_checkout()  # Proceed to Checkout
        self._check_accessibility(page, page.url)

    def _check_accessibility(self, page: Page, url: str):
        page.goto(url)

        self._inject_axe(page)

        page.evaluate("axe.run().then(results => window.axeResults = results);")
        results = page.evaluate("() => window.axeResults")

        if results['violations']:
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
