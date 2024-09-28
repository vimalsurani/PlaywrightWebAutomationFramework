from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.checkout_button = "//button[@id='checkout']"

    def proceed_to_checkout(self):
        # Check if the checkout button is visible before clicking
        if self.page.is_visible(self.checkout_button):
            self.page.click(self.checkout_button)
        else:
            raise Exception("Checkout button is not visible.")
