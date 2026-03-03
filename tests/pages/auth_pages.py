from random import randint
from .page import BasePage


class AuthSignInPage(BasePage):
    SUB_DIRECTORY = "/auth/signin"
    # Selectors
    EMAIL_PHONE = "#email"
    PASSWORD = "#password"
    LOGIN_BUTTON = "button[type='submit']"

    def login(self, username: str, password: str):
        self.fill(self.EMAIL_PHONE, username)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)


class AuthAccountPage(BasePage):
    SUB_DIRECTORY = "/auth/account"

    def check_account_num(self) -> int:
        return self.page.locator("[data-testid^='sub-account-option']").count()


    def select_random_account(self):
        accounts = self.page.locator("[data-testid^='sub-account-option']")
        count = accounts.count()
        if count <= 1:
            raise ValueError(f"Expected multiple accounts but found {count}; update test data")
        random_index = randint(0, count - 1)
        accounts.nth(random_index).click()
