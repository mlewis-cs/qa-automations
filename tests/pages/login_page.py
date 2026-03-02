from asyncio import sleep

from .page import BasePage


class LoginPage(BasePage):
    SUB_DIRECTORY = "/login"
    # Selectors
    EMAIL_PHONE = "#login"
    PASSWORD = "#password"
    LOGIN_BUTTON = "button[type='submit']"

    def login(self, username: str, password: str):
        self.fill(self.EMAIL_PHONE, username)
        self.click(self.LOGIN_BUTTON)
        # Wait for dom to load after clicking login button
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        