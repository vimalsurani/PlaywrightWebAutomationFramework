from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        # Locators as class attributes
        self.sort_dropdown = 'select.product_sort_container'
        self.item_name_selector = '.inventory_item_name'
        self.item_price_selector = '.inventory_item_price'
        self.add_to_cart_button = '.btn_inventory'
        self.cart_icon = '.shopping_cart_link'

    def sort_items_by(self, order: str):
        """Sort items based on the specified order."""
        sort_options = {
            'az': 'az',  # Sort A-Z
            'za': 'za',  # Sort Z-A
            'lohi': 'lohi',  # Sort low to high price
            'hilo': 'hilo'  # Sort high to low price
        }
        if order in sort_options:
            self.page.select_option(self.sort_dropdown, sort_options[order])
        else:
            raise ValueError(f"Invalid sort order: {order}")

    def get_item_names(self):
        """Return a list of item names."""
        item_names = [item.inner_text() for item in self.page.query_selector_all(self.item_name_selector)]
        return item_names

    def get_item_prices(self):
        """Return a list of item prices as floats."""
        item_prices = [float(price.inner_text().replace('$', '')) for price in
                       self.page.query_selector_all(self.item_price_selector)]
        return item_prices

    def add_items_to_cart(self, count: int):
        """Add a specified number of items to the cart."""
        items = self.page.query_selector_all(self.add_to_cart_button)
        if count > len(items):
            raise ValueError(f"Cannot add {count} items, only {len(items)} available.")

        for item in items[:count]:
            item.click()

    def go_to_cart(self):
        """Navigate to the cart page."""
        self.page.click(self.cart_icon)

    def validate_items_sorted(self, order: str):
        """Validate that items are sorted as expected after sorting."""
        if order in ['az', 'za']:
            item_names = self.get_item_names()
            if order == 'az':
                assert item_names == sorted(item_names), "Items are not sorted A-Z"
            else:
                assert item_names == sorted(item_names, reverse=True), "Items are not sorted Z-A"
        elif order in ['lohi', 'hilo']:
            item_prices = self.get_item_prices()
            if order == 'lohi':
                assert item_prices == sorted(item_prices), "Items are not sorted low to high"
            else:
                assert item_prices == sorted(item_prices, reverse=True), "Items are not sorted high to low"
