from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = 'input[id="user-name"]'
        self.password_input = 'input[id="password"]'
        self.login_button = 'input[id="login-button"]'
        self.error_message = 'div[class="error-message-container"]'

    def enter_username(self, username: str):
        self.page.fill(self.username_input, username)

    def enter_password(self, password: str):
        self.page.fill(self.password_input, password)

    def click_login(self):
        self.page.click(self.login_button)

    def login(self, username: str = 'standard_user', password: str = 'secret_sauce'):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

        if self.page.is_visible(self.error_message):
            raise Exception("Login failed: Invalid username or password")
