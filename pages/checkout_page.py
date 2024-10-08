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
        self.checkout_complete_message = 'h2[class="complete-header"]'  # Example success message locator

    def fill_first_name(self, first_name: str):
        """Fill in the first name field."""
        self.page.fill(self.first_name_input, first_name)

    def fill_last_name(self, last_name: str):
        """Fill in the last name field."""
        self.page.fill(self.last_name_input, last_name)

    def fill_postal_code(self, postal_code: str):
        """Fill in the postal code field."""
        self.page.fill(self.postal_code_input, postal_code)

    def click_continue(self):
        """Click the continue button to proceed to the next step."""
        self.page.click(self.continue_button)

    def fill_checkout_form(self, first_name: str, last_name: str, postal_code: str):
        """Fill the checkout form with user details."""
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_postal_code(postal_code)
        self.click_continue()

    def finish_checkout(self):
        """Complete the checkout process by clicking the finish button."""
        self.page.click(self.finish_button)

    def verify_checkout_complete(self):
        """Verify if checkout is completed successfully."""
        assert self.page.is_visible(self.checkout_complete_message), "Checkout was not completed successfully"
