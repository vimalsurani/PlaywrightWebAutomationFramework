from playwright.sync_api import Page


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        # Store locators as class attributes for easier reference
        self.first_name_input = 'input[data-test="firstName"]'
        self.last_name_input = 'input[data-test="lastName"]'
        self.postal_code_input = 'input[data-test="postalCode"]'
        self.continue_button = 'input[data-test="continue"]'
        self.finish_button = 'button[data-test="finish"]'
        self.checkout_complete_message = 'h2[class="complete-header"]'

    def fill_first_name(self, first_name: str):
        self.page.fill(self.first_name_input, first_name)

    def fill_last_name(self, last_name: str):
        self.page.fill(self.last_name_input, last_name)

    def fill_postal_code(self, postal_code: str):
        self.page.fill(self.postal_code_input, postal_code)

    def click_continue(self):
        self.page.click(self.continue_button)

    def fill_checkout_form(self, first_name: str, last_name: str, postal_code: str):
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_postal_code(postal_code)
        self.click_continue()

    def finish_checkout(self):
        self.page.click(self.finish_button)

    def verify_checkout_complete(self):
        assert self.page.is_visible(self.checkout_complete_message), "Checkout was not completed successfully"
